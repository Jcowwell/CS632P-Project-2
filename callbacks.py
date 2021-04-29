
import json
from app import app
# NOTE: - Load Plotly libraries
import plotly.io as pio
import plotly.express as px
# NOTE: - Load Dash libraries
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
# NOTE: - Load Project Libraries
from components import filter_table, preview_table, graph
from constants import ADJ_CLOSE, DATE, DEFAULT_FEATURE, DEFAULT_STOCK, EMPTY_DIV, ERROR_DIV, STOCK
from callback_helper import dump_dataframe, filter_dataframe_by_column_value, get_numerical_columns, get_unique_values, paginate, process_file, filter_dataframe_columns, load_dataframe

# SECTION: - Callback Functions
# NOTE: - Callback to Show File was Uploaded
@app.callback(Output('upload', 'children'),
              [Input('upload', 'contents')],
              [State('upload', 'filename')]
              )  
def display_contents_received(file_content, filename):
    # If File content has not been uploaded show the option to upload.
    children= [html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ])]
    # If File content has uploaded, Show It!
    if file_content is not None:
        children = [html.Div(['%s Uploaded' % (filename)])]
    return children

# NOTE: - Callback to Parse Data, Show Filter Datatable and Store Parse Data Contents to a Itermediate Div
@app.callback([Output('filter-datatable-container', 'children'),
              Output('dataframe-value','children'),
              Output('stock-values','children'),
              Output('feature-values', "children")],
              [Input('parse-button','n_clicks')],
              [State('upload', 'contents'),
              State('upload', 'filename'),
              State('upload', 'last_modified')]
              )
def display_filter_table(n_clicks, file_content, filename, file_date):
    # Let's not do anyhting unless the Button is clicked or no file_content to upload.
    if not n_clicks or file_content is None:
        raise PreventUpdate

    if file_content is not None:
        # Get Dataframe from Upload
        dataframe = process_file(file_content,filename)
        if dataframe is None:
            # Show soemthing went wrong if Dataframe wasn't made
            return ERROR_DIV, EMPTY_DIV, EMPTY_DIV, EMPTY_DIV
        
        # Convert dataframe to JSON Object to access in other Callbacks
        dataframe_json = dump_dataframe(dataframe=dataframe)
        # Get JSON lists of unique Stock values from Dataframe 
        stocks_json = json.dumps(get_unique_values(dataframe=dataframe, column_name=STOCK))
        # Get JSON lists of numerical columns from Dataframe
        features_json = json.dumps(get_numerical_columns(dataframe=dataframe))
        print(filter_table(dataframe))
        return filter_table(dataframe), dataframe_json, stocks_json, features_json
        
# TODO
# NOTE: - Callback to show Preview Data Table 
@app.callback([Output('permitted-columns','children'),
              Output('preview-datatable-container', 'children'),
              Output('graph-plot-container', 'children')],
              [Input('filter-button','n_clicks')],
              [State('dataframe-value','children'),
              State('stock-values','children'),
              State('feature-values','children'),
              State('filter-table','data'),
              State('filter-table','derived_virtual_selected_rows')]
              )
def display_data(n_clicks , dataframe_json, stocks_json, features_json, filter_table_data, selected_rows):
    # Let's not Update unless the Button is clicked.
    if not n_clicks:
        raise PreventUpdate

    # Lists of Wanted Columns.
    permitted_columns = [row for index, row in enumerate(filter_table_data) if index not in selected_rows]
    # Globally Stored Dataframe
    dataframe = load_dataframe(dataframe_json=dataframe_json)
    # Filtered Dataframe based on Allowed Columns
    filtered_dataframe = filter_dataframe_columns(dataframe=dataframe, permitted_columns=permitted_columns)

    # If the filtered dataframe is empty...Houson we have a problem
    if filtered_dataframe is None or filtered_dataframe.empty: 
        return EMPTY_DIV, EMPTY_DIV, ERROR_DIV
    
    # Lists of Stocks from JSON Object
    stocks = json.loads(stocks_json)

    # Lists of (numerical) columns from JSON Object
    features = json.loads(features_json)

    # Title for graph
    title = "%s vs %s" % (DEFAULT_FEATURE, DEFAULT_STOCK)
    # Figure for Graph Plot
    fig = px.line(dataframe, x=DATE, y=ADJ_CLOSE, color=STOCK, template=pio.templates['seaborn'], title=title)

    # Paginate Dataframe
    filtered_dataframe = paginate(dataframe=filtered_dataframe, page_current=0, page_size=0)

    # Dump Lists of Wanted Columns into a JSON Object
    permitted_columns_json = json.dumps(permitted_columns)
    # Preview Table
    preview_table_ = preview_table(dataframe=filtered_dataframe, dropdown_options=stocks)
    # Graph
    graph_ = graph(fig=fig, feature_dropdown_option=features, securities_dropdown_option=stocks)
    
    #NOTE: - permitted_columns_json JSON Object must be returned before the preivew table or the update callback for the preview_table will be called and fuck shit up.  
    return permitted_columns_json, preview_table_, graph_

# NOTE: - Callback to Update Preview Table Page 
@app.callback(
    Output('preview-table', 'data'),
    [Input('preview-table', "page_current"),
    Input('preview-table', "page_size"),
    Input('curve-identifier-dropdown', "value")],
    [State('dataframe-value', "children"),
    State('permitted-columns','children')],
    )
def update_preview_table(page_current, page_size, curve_identifier, dataframe_json, permitted_columns_json):

    if permitted_columns_json is not None:
        # Dump Lists of Wanted Columns
        permitted_columns = json.loads(permitted_columns_json)
    # Dump Dataframe from JSON Object 
    dataframe = load_dataframe(dataframe_json=dataframe_json)
    # Filter Dataframe based on lists of wanted columns
    filtered_dataframe = filter_dataframe_columns(dataframe=dataframe, permitted_columns=permitted_columns)
    if curve_identifier != []:
        # Filtered Dataframe based on inputed stock values
        filtered_dataframe = filter_dataframe_by_column_value(dataframe=filtered_dataframe, column=STOCK, value=curve_identifier)
    # Paginate Filtered Dataframe
    filtered_dataframe = paginate(dataframe=filtered_dataframe, page_current=page_current, page_size=page_size)

    return filtered_dataframe.to_dict('records')

# TODO
# NOTE: - Callback to Update Graph based on Dropdown Values
@app.callback(
    Output('graph', 'figure'),
    [Input('feature', "value"),
    Input('securities', "value")],
    [State('dataframe-value', "children")],
    )
def update_graph(feature, securities, dataframe_json):
    if feature is None or securities is None or securities == []:
        # Houson... We got a problem
        return {}

    # Globally Stored Dataframe
    dataframe = load_dataframe(dataframe_json=dataframe_json)

    # Filter Stocks from securities Dropdown
    filtered_dataframe = filter_dataframe_by_column_value(dataframe=dataframe, column=STOCK, value=securities)

    # Title for Graph
    title = "%s vs %s" % (DEFAULT_FEATURE, DEFAULT_STOCK)
    # Figure for Graph
    fig = px.line(filtered_dataframe, x=DATE, y=feature, color=STOCK, template=pio.templates['seaborn'], title=title)

    return fig

# !SECTION