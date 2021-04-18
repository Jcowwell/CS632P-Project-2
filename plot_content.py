# SECTION: - Imports
# REVIEW: - Optimize Imports

# NOTE: - File Processing Libraries
import json
from callback_helper import process_file, process_data
from styles import app_style, hide_div, table_style, center_div_contents, button_style, upload_style
from constants import DATATYPES, _DATATYPES, COLUMN_NAMES, PREVIEW_DROPDOWN_HEADER, FEATURE_NAME_TO_PLOT, SECURITIES_TO_DISPLAY, DATE, PAGE_SIZE, ERROR_DIV, STOCK
# NOTE: - Load Dash libraries
import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# !SECTION

app = dash.Dash('Hello Dash!', suppress_callback_exceptions=True)

# SECTION: - App Layout
# NOTE: - App CSS
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# NOTE: - Dash-Layout component
app.layout = html.Div(
    [
        # File Upload Element
        dcc.Upload(
            id='upload',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            multiple=False,
            style=upload_style
        ),

        # Parse Data Button
        html.Button(
            'Parse Data',
            id='parse-button',
            n_clicks=0, 
            style=button_style
        ), 

        html.Hr(),  # horizontal line

        #  Div object for Filter Datatable Components
        html.Div(id='filter-datatable-container'),

        # Div object for Preview Datatable Components
        html.Div(id='preview-datatable-container'),

        # Div object for Graph Plot Components
        html.Div(id='graph-plot-container'),

        # Hidden div that stores the intermediate value (in this case DataFrames)
        html.Div(id='intermediate-value', style=hide_div),

        # Hidden div that stores a JSON representation of a lists of Permtted Columns according to User input
        html.Div(id='permitted-columns', style=hide_div),

        # Hidden div that stores a JSON representation of a lists of Permtted Columns according to User input
        html.Div(id='stock-values', style=hide_div),

        # Hidden div that stores a JSON representation of a lists of Permtted Columns according to User input
        html.Div(id='feature-values', style=hide_div)
    ], 
    style=app_style
)
# !SECTION

# SECTION: - Component Functions 

''' 
NOTE: - Returns a Div object that consists of a Datatable responsible for allowing the user to select an
appropriate datatype for an input file's columns and ignore selected columns. 
'''
# NOTE: - Function for Filter Datatable and Related Components
def filter_table(dataframe):
    header = [{COLUMN_NAMES:column, _DATATYPES:'String'} for column in dataframe.columns]
    # data = dataframe.to_dict('records')
    return html.Div([
        dash_table.DataTable(
            id='filter-table',
            columns=[
                {"name": COLUMN_NAMES, "id": COLUMN_NAMES, 'editable':False},
                {"name": _DATATYPES, "id": _DATATYPES,  'presentation': 'dropdown'},
            ],
            data=header,
            dropdown = {
                _DATATYPES: {
                    'options': [
                        {'label': datatype, 'value': datatype} for datatype in DATATYPES
                    ],
                },
            },
            row_selectable="multi",
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,
            editable=True,
            style_table=table_style,
            style_cell = {'textAlign': 'left'},   
        ),

        html.Hr(),  # horizontal line

        html.Button('Submit', id='filter-button', n_clicks=0, 
            style=button_style,
        ), 

        html.Hr(),  # horizontal line
    ],
        style=center_div_contents
    )

''' 
NOTE: - Returns a Div object that consists of a Multi-Value Dropdown and a 
Datatable responsible for previewing the input and filtered data based on 
the filter table and forementioned dropdown component.
'''
# NOTE: - Function for Preview Datatable and Related Components
# TODO
def preview_table(dataframe, dropdown_options):
    
    return html.Div([
        # Header
        html.H2(PREVIEW_DROPDOWN_HEADER),

        # Curve Identifier to Display Dropdown
        dcc.Dropdown(
            id='curve-identifier-dropdown',
            options=[{'label': option, 'value': option} for option in dropdown_options],
            value=['AAPL'],
            placeholder="Select a Stock to Display",
            multi=True,
            searchable=False,
        ),

        # Preview Table
        dash_table.DataTable(
            id='preview-table',
            data=dataframe.to_dict('records'),
            columns=[{'name': i, 'id': i,} for i in dataframe.columns],
            style_cell = {'textAlign': 'left'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in dataframe.columns
            ],
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
            style_table=table_style,
            style_as_list_view=True,
        ),

        html.Hr(),  # horizontal line

        # # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ],
        style=center_div_contents,
    )

''' 
NOTE: - Returns a Div object that consists of a Single-Value Dropdown, 
a Multi-Value Dropdown and a Plot Graph that corresponds with what's shown in
the Preview Datatable Component.
'''
# NOTE: - Function for Graph Plot and Related Components
# TODO
def graph(data):
        # TODO - Insert Feature Name to Plot here
        dcc.Dropdown(
            id='feature-dropdown',
            options=[{'label': option, 'value': option} for option in []],
            # TODO: Convert to Constant String
            value=['AAPL'],
            # TODO: COnvert to Constant String
            placeholder="Select a Feature to Plot",
        ),
        # TODO - Insert Securities to Display here
        dcc.Dropdown(
            id='securities-dropdown',
            options=[{'label': option, 'value': option} for option in []],
            value=['AAPL'],
            # TODO: Convert to Constant String
            placeholder="Select a Stock to Display",
            multi=True,
            searchable=False,
        ),
        # TODO - Insert Graph Plot Here
        # dcc.Graph(
        #     id='graph'
        # )
# !SECTION

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
              Output('intermediate-value','children'),
              Output('stock-values','children'),
              Output('feature-values', "value")],
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
        stocks_json = json.dumps(dataframe['Stock'].unique().tolist())
        # TODO: - features_json = get_numerical_columns()
        return filter_table(dataframe), dataframe_json, stocks_json
        
# TODO
# NOTE: - Callback to show Preview Data Table 
@app.callback([Output('permitted-columns','children'),
              Output('preview-datatable-container', 'children')],
              [Input('filter-button','n_clicks')],
              [State('intermediate-value','children'),
              State('stock-values','children'),
              State('filter-table','data'),
              State('filter-table','derived_virtual_selected_rows')]
              )
def display_preview_table(n_clicks , dataframe_json, stocks_json, filter_table_data, selected_rows, features, selected):
    if not n_clicks:
        raise PreventUpdate

    permitted_data = [row for index, row in enumerate(filter_table_data) if index not in selected_rows]

    dataframe = process_data(permitted_data=permitted_data, dataframe_json=dataframe_json)

    if dataframe is None: 
        return ERROR_DIV
    
    stocks = json.loads(stocks_json)
    
    # Invoke Dropview & Graph Components Display Function

    dataframe = dataframe.iloc[0 * PAGE_SIZE: (1) * PAGE_SIZE]

    return  json.dumps(permitted_data), preview_table(dataframe=dataframe, dropdown_options=stocks)

# NOTE: - Callback to Update Preview Table Page 
# FIXME: - WINDOWS 10 MICROSOFT EDGE ISSUE: State('permitted-columns','children')] returns none?
@app.callback(
    Output('preview-table', 'data'),
    [Input('preview-table', "page_current"),
    Input('preview-table', "page_size"),
    Input('curve-identifier-dropdown', "value")],
    [State('intermediate-value', "children"),
    State('permitted-columns','children')],
    )
def update_preview_table(page_current, page_size, curve_identifier, dataframe_json, permitted_data_json):
    permitted_data = []
    if permitted_data_json is not None:
        permitted_data = json.loads(permitted_data_json)
    dataframe = process_data(permitted_data=permitted_data, dataframe_json=dataframe_json)
    if curve_identifier != []:
        is_curve_identifier = dataframe[STOCK].isin(curve_identifier)
        dataframe = dataframe[is_curve_identifier]
    return dataframe[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

# TODO
# NOTE: - Callback to Display Graph 
@app.callback(
    Output('graph', 'figure'),
    [Input('preview-table', "data")],
    )
def display_graph(dataframe):
    # Get Volume and Data Columns based on Value Types for feature-dropdown component
    # Use stock-values for securities-dropdown dropdown
    # Invoke Graph Figure Function that returns a Graph Figure. 
    print("Here")
    return
# !SECTION

# SECTION: - Launch Application
# NOTE: - Launch Application in Debugger Mode
app.run_server(debug=True)
# NOTE: - Launch Application in Normal Mode
# app.run_server()
# !SECTION
