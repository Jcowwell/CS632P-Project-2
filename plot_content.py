# SECTION: - Imports
# REVIEW: - Optimize Imports

# NOTE: - File Processing Libraries
import base64
import datetime
import io
from styles import button_style, upload_style
from constants import DATATYPES, COLUMN_NAMES, DATATYPE, PREVIEW_DROPDOWN_HEADER, FEATURE_NAME_TO_PLOT, SECURITIES_TO_DISPLAY, DATE
# NOTE: - Load Dash libraries
import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
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
                'Drag or Drop or ',
                html.A('Select Files')
            ]),
            style=upload_style
        ),

        # Parse Data Button
        html.Button(
            id='parse_button', 
            name='Parse Data', 
            n_clicks=0, 
            style=button_style
        ), 

        #  Div object for Filter Datatable Components
        html.Div(id='filter_datatable_container'),

        # Div object for Preview Datatable Components
        html.Div(id='preview_datatable_container'),

        # Div object for Graph Plot Components
        html.Div(id='graph_plot_container'),
    ], 


    style={'width': '300'}
)
# !SECTION

# SECTION: - Component Functions 

''' 
NOTE: - Returns a Div object that consists of a Datatable responsible for allowing the user to select an
appropriate datatype for an input file's columns and ignore selected columns. 
'''
# NOTE: - Function for Filter Datatable and Related Components
def filter_table(data_frame):
    header = []
    for column in data_frame.columns:
        header.append({
            COLUMN_NAMES:column,
        })
    data = data_frame.to_dict('records')
    return html.Div([
        dash_table.DataTable(
            id='filter_table',
            columns=[
                {"name": COLUMN_NAMES, "id": COLUMN_NAMES, 'editable':False},
                {"name": DATATYPE, "id": DATATYPE,  'presentation': 'dropdown'},
            ],
            data=header,
            dropdown = {
                DATATYPE: {
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
        html.Button('Submit', id='filter_button', n_clicks=0, 
            style=button_style,
        ), 
    ],
        style={'textAlign':'center'},
    )

''' 
NOTE: - Returns a Div object that consists of a Multi-Value Dropdown and a 
Datatable responsible for previewing the input and filtered data based on 
the filter table and forementioned dropdown component.
'''
# NOTE: - Function for Preview Datatable and Related Components
# TODO
def preview_table(data_frame):
    return html.Div([
        # Header
        html.H1(PREVIEW_DROPDOWN_HEADER),

        # TODO - Insert logic to get Unique 'Stock' in a lists for Curve Identifier Dropdown here

        # Curve Identifier to Display Dropdown
        dcc.Dropdown(
            id='curve-identifier',
            options=[{}],
            value='',
        ),

        # Preview Table
        # FIXME 
        dash_table.DataTable(
            id='datatable',
            data=data_frame.to_dict('records'),
            columns=[{'name': i, 'id': i,} for i in data_frame.columns],
            style_cell = {'textAlign': 'left'},
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
Parses CSV and XLS data.
'''
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            return filter_table(df)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
# !SECTION

# SECTION: - Callback Functions
# FIXME: - Set Callback trigger to Button
@app.callback(Output('filter_datatable_container', 'columns'),
              Input('upload', 'contents'),
              State('upload', 'filename'),
              State('upload', 'last_modified'))
def display_filter_table(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(list_of_contents, list_of_names, list_of_dates)]
        return children

# TODO
def display_preview_table():
    return
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
