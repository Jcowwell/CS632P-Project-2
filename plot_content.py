# SECTION: - Imports
# REVIEW: - Optimize Imports

# NOTE: - File Processing Libraries
import io
import json
import base64
import datetime
from styles import app_style, button_style, upload_style
from constants import DATATYPES, _DATATYPES, COLUMN_NAMES, PREVIEW_DROPDOWN_HEADER, FEATURE_NAME_TO_PLOT, SECURITIES_TO_DISPLAY, DATE, PAGE_SIZE
# NOTE: - Load Dash libraries
import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# !SECTION

app = dash.Dash('Hello Dash!')

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
            id='parse_button',
            n_clicks=0, 
            style=button_style
        ), 

        html.Hr(),  # horizontal line

        #  Div object for Filter Datatable Components
        html.Div(id='filter_datatable_container'),

        # Div object for Preview Datatable Components
        html.Div(id='preview_datatable_container'),

        # Div object for Graph Plot Components
        html.Div(id='graph_plot_container'),

        # Hidden div that stores the intermediate value (in this case DataFrames)
        html.Div(id='intermediate-value', style={'display': 'none'}),

        # Hidden div that stores the intermediate value (in this case DataFrames)
        html.Div(id='permitted-columns', style={'display': 'none'})
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
    data = dataframe.to_dict('records')
    return html.Div([
        dash_table.DataTable(
            id='filter_table',
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
            style_cell = {'textAlign': 'left'},    
        ),

        html.Hr(),  # horizontal line

        html.Button('Submit', id='filter_button', n_clicks=0, 
            style=button_style,
        ), 

        html.Hr(),  # horizontal line
    ],
        style=app_style
    )

''' 
NOTE: - Returns a Div object that consists of a Multi-Value Dropdown and a 
Datatable responsible for previewing the input and filtered data based on 
the filter table and forementioned dropdown component.
'''
# NOTE: - Function for Preview Datatable and Related Components
# TODO
def preview_table(dataframe):
    return html.Div([
        # Header
        html.H1(PREVIEW_DROPDOWN_HEADER),

        # TODO - Insert logic to get Unique 'Stock' in a lists for Curve Identifier Dropdown here

        # Curve Identifier to Display Dropdown
        # TODO - Add Option Logic
        # dcc.Dropdown(
        #     id='curve-identifier',
        #     options=[{}],
        #     value='',
        # ),

        # Preview Table
        # FIXME 
        dash_table.DataTable(
            id='preview_table',
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
            style_as_list_view=True,
        ),

        html.Hr(),  # horizontal line

        # # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])

''' 
NOTE: - Returns a Div object that consists of a Single-Value Dropdown, 
a Multi-Value Dropdown and a Plot Graph that corresponds with what's shown in
the Preview Datatable Component.
'''
# NOTE: - Function for Graph Plot and Related Components
# TODO
def graph(data):
    return
        # TODO - Insert Feature Name to Plot here
        # TODO - Insert Securities to Display here
        # TODO - Insert Graph Plot Here
# !SECTION

# SECTION: - Callback Function Helpers

''' 
NOTE: - Adopted from: https://dash.plotly.com/dash-core-components/upload
Processes CSV and XLS Content Data
'''
def process_file(contents,filename):
    content_type, content_string = contents.split(',')

    decoded_content = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            return pd.read_csv(
                io.StringIO(decoded_content.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            return pd.read_excel(io.BytesIO(decoded_content))
    except Exception as e:
        print(e)
    return None
''' 
NOTE: -
Returns a Dataframe Object from json data
'''
def json_to_dataframe(dataframe_json):
    return pd.read_json(dataframe_json, orient='split')
''' 
NOTE: -
Process Non-Ignored Data and return a Div Object consiting of a Datatable.
'''
def process_data(permitted_data, dataframe_json):
    if not permitted_data:
        return None
    dataframe = pd.read_json(dataframe_json, orient='split')
    columns = [column['Column Names'] for column in permitted_data] 
    _dataypes = [__datatypes['DataTypes'] for __datatypes in permitted_data]

    # FIXME: - Convert Column Data to DataType based on Index. Perhaps use a Function. 

    return dataframe[columns]
    
# !SECTION

# SECTION: - Callback Functions

# NOTE: - Callback to Show File was Uploaded
@app.callback(Output('upload', 'children'),
              Input('upload', 'contents'),
              State('upload', 'filename'),
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
@app.callback(Output('filter_datatable_container', 'children'),
              Output('intermediate-value','children'),
              Input('parse_button','n_clicks'),
              State('upload', 'contents'),
              State('upload', 'filename'),
              State('upload', 'last_modified')
              )
def display_filter_table(n_clicks, file_content, filename, file_date):
    if not n_clicks:
        raise PreventUpdate
    if file_content is not None:
        df = process_file(file_content,filename)
        if df is None:
            return html.Div([
            'There was an error processing this file.'
            ]), html.Div()
        df_json = df.to_json(date_format='iso', orient='split')
        return filter_table(df), df_json 
        
# TODO
# NOTE: - Callback to show Preview Data Table 
@app.callback(Output('preview_datatable_container', 'children'),
              Output('permitted-columns','children'),
              Input('filter_button','n_clicks'),
              State('intermediate-value','children'),
              State('filter_table','data'),
              State('filter_table','derived_virtual_selected_rows'),
              State('filter_table','dropdown.value'),
              )
def display_preview_table(n_clicks , dataframe_json, filter_table_data, selected_rows, dropdown):
    if not n_clicks:
        raise PreventUpdate

    print("Filtered Data: %s" % filter_table_data)
    print("Selected Rows: %s" % selected_rows)
    print("Dropdown: %s" % dropdown)

    permitted_data = [row for index, row in enumerate(filter_table_data) if index not in selected_rows]

    dataframe = process_data(permitted_data=permitted_data, dataframe_json=dataframe_json)

    return preview_table(dataframe=dataframe), json.dumps(permitted_data)

@app.callback(
    Output('preview_table', 'data'),
    Input('preview_table', "page_current"),
    Input('preview_table', "page_size"),
    State('intermediate-value', "children"),
    State('permitted-columns','children'),
    )
def update_preview_table(page_current, page_size, dataframe_json, permitted_data_json):
    permitted_data = json.loads(permitted_data_json)
    dataframe = process_data(permitted_data=permitted_data, dataframe_json=dataframe_json)
    return dataframe[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

# TODO
def display_graph():
    return
# !SECTION

# SECTION: - Launch Application
# NOTE: - Launch Application in Debugger Mode
app.run_server(debug=True)
# NOTE: - Launch Application in Normal Mode
# app.run_server()
# !SECTION
