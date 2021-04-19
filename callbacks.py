
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
from constants import ADJ_CLOSE, DATE, DEFAULT_FEATURE, DEFAULT_STOCK, PAGE_SIZE, ERROR_DIV, STOCK
from callback_helper import get_numerical_columns, get_unique_values, process_file, filter_dataframe, unload_dataframe

# SECTION: - Callback Functions
# NOTE: - Callback to Show File was Uploaded
@app.callback(Output('upload', 'children'),
              [Input('upload', 'contents')],
              [State('upload', 'filename')]
              )  
def display_contents_received(file_content, filename):
    if file_content is None:
        children= [html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ])]
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
    if not n_clicks:
        raise PreventUpdate
    if file_content is not None:
        dataframe = process_file(file_content,filename)
        if dataframe is None:
            return ERROR_DIV
        dataframe_json = dataframe.to_json(date_format='iso', orient='split')
        # TODO: - Convert to more abstract function
        stocks_json = json.dumps(get_unique_values(dataframe=dataframe, column_name=STOCK))
        features_json = json.dumps(get_numerical_columns(dataframe=dataframe))
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
def display_preview_table(n_clicks , dataframe_json, stocks_json, features_json, filter_table_data, selected_rows):
    if not n_clicks:
        raise PreventUpdate

    permitted_data = [row for index, row in enumerate(filter_table_data) if index not in selected_rows]

    dataframe = unload_dataframe(dataframe_json=dataframe_json)

    filtered_dataframe = filter_dataframe(permitted_data=permitted_data, dataframe=dataframe)

    if filtered_dataframe is None: 
        return ERROR_DIV
    
    stocks = json.loads(stocks_json)

    features = json.loads(features_json)

    title = "%s vs %s" % (DEFAULT_FEATURE, DEFAULT_STOCK)
    fig = px.line(dataframe, x=DATE, y=ADJ_CLOSE, color=STOCK, template=pio.templates['seaborn'], title=title)

    filtered_dataframe = filtered_dataframe.iloc[0 * PAGE_SIZE: (1) * PAGE_SIZE]

    return json.dumps(permitted_data), preview_table(dataframe=filtered_dataframe, dropdown_options=stocks), graph(fig=fig, feature_dropdown_option=features, securities_dropdown_option=stocks)

# NOTE: - Callback to Update Preview Table Page 
@app.callback(
    Output('preview-table', 'data'),
    [Input('preview-table', "page_current"),
    Input('preview-table', "page_size"),
    Input('curve-identifier-dropdown', "value")],
    [State('dataframe-value', "children"),
    State('permitted-columns','children')],
    )
def update_preview_table(page_current, page_size, curve_identifier, dataframe_json, permitted_data_json):
    permitted_data = []
    if permitted_data_json is not None:
        permitted_data = json.loads(permitted_data_json)
    dataframe = unload_dataframe(dataframe_json=dataframe_json)
    filtered_dataframe = filter_dataframe(permitted_data=permitted_data, dataframe=dataframe)
    if curve_identifier != []:
        is_curve_identifier = filtered_dataframe[STOCK].isin(curve_identifier)
        filtered_dataframe = filtered_dataframe[is_curve_identifier]
    return filtered_dataframe[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

# TODO
# NOTE: - Callback to Update Graph based on Dropdown Values

# !SECTION