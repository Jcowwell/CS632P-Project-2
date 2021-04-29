# SECTION: - Imports
# REVIEW: - Optimize Imports
# NOTE: - Load Dash libraries
from typing import OrderedDict
from callback_helper import get_dataframe_column_datatype
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
# NOTE: - Load Project Libraries
from styles import table_style, center_div_contents, filter_div_contents, button_style, dropdown_style
from constants import ADJ_CLOSE, DATATYPES, DATATYPES_CONVERSION_OPTIONS, DATATYPE_MAP, DATE, DEFAULT_FEATURE, DEFAULT_STOCK, EXCHANGE, FEATURE_DROPDOWN_PLACEHOLDER, FILTER_TABLE_TITLE, STOCK, STOCK_DROPDOWN_PLACEHOLDER, DATATYPES_, COLUMN_NAMES, PREVIEW_DROPDOWN_HEADER, FEATURE_NAME_TO_PLOT, SECURITIES_TO_DISPLAY, PAGE_SIZE, VOLUME
# !SECTION

# SECTION: - Component Functions 
''' 
NOTE: - Returns a Div object that consists of a Datatable responsible for allowing the user to select an
appropriate datatype for an input file's columns and ignore selected columns. 
'''
# NOTE: - Function for Filter Datatable and Related Components
def filter_table(dataframe):
    header = [{COLUMN_NAMES:column, DATATYPES_:'String'} for column in dataframe.columns]
    data = get_dataframe_column_datatype(dataframe=dataframe)
    df_per_row_dropdown = pd.DataFrame(OrderedDict([
    ('Column Names', [DATE, VOLUME, ADJ_CLOSE, STOCK, EXCHANGE]),
    ('DataTypes', ['Date', 'String', 'String', 'Float', 'Integer']),
    ]))
    print(data)
    return html.Div([

        html.H3(FILTER_TABLE_TITLE),

        dash_table.DataTable(
            id='filter-table',
            columns=[
                {"name": COLUMN_NAMES, "id": COLUMN_NAMES, 'editable':False},
                {"name": DATATYPES_, "id": DATATYPES_,  'presentation': 'dropdown'},
            ],
            data=df_per_row_dropdown.to_dict('records'),
            dropdown_conditional=[
                
                {
                'if' : {
                        'column_id': DATATYPES_,
                        'filter_query': '{%s} eq "%s"' % (COLUMN_NAMES, DATE)
                },
                'options' : [
                    {'label': datatype, 'value': DATATYPE_MAP[datatype]}
                            for datatype in data[DATE]
                ],
                "clearable" : False
            },
            {
                'if' : {
                        'column_id': DATATYPES_,
                        'filter_query': '{%s} eq "%s"' % (COLUMN_NAMES, VOLUME)
                },
                'options' : [
                    {'label': datatype, 'value': DATATYPE_MAP[datatype]}
                            for datatype in data[VOLUME]
                ],
                "clearable" : False
            },
            {
                'if' : {
                        'column_id': DATATYPES_,
                        'filter_query': '{%s} eq "%s"' % (COLUMN_NAMES, ADJ_CLOSE)
                },
                'options' : [
                    {'label': datatype, 'value': DATATYPE_MAP[datatype]}
                            for datatype in data[ADJ_CLOSE]
                ],
                "clearable" : False
            },
            {
                'if' : {
                        'column_id': DATATYPES_,
                        'filter_query': '{%s} eq "%s"' % (COLUMN_NAMES, STOCK)
                },
                'options' : [
                    {'label': datatype, 'value': DATATYPE_MAP[datatype]}
                            for datatype in data[STOCK]
                ],
                "clearable" : False
            },
            {
                'if' : {
                        'column_id': DATATYPES_,
                        'filter_query': '{%s} eq "%s"' % (COLUMN_NAMES, EXCHANGE)
                },
                'options' : [
                    {'label': datatype, 'value': DATATYPE_MAP[datatype]}
                            for datatype in data[EXCHANGE]
                ],
                "clearable" : False
            }],
            row_selectable="multi",
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,
            editable=True,
            style_table=table_style,
            style_cell = {'textAlign': 'left'},   
        ),

        html.Button('Submit', id='filter-button', n_clicks=0, 
            style=button_style,
        ), 

        html.Hr(),  # horizontal line
    ],
        style=filter_div_contents
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
        html.H3(PREVIEW_DROPDOWN_HEADER),

        # Curve Identifier to Display Dropdown
        dcc.Dropdown(
            id='curve-identifier-dropdown',
            options=[{'label': option, 'value': option} for option in dropdown_options],
            value=[DEFAULT_STOCK],
            placeholder=STOCK_DROPDOWN_PLACEHOLDER,
            multi=True,
            searchable=False,
            clearable=False,
            style=dropdown_style,
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
    ],
        style=center_div_contents,
    )

''' 
NOTE: - Returns a Div object that consists of a Single-Value Dropdown, 
a Multi-Value Dropdown and a Plot Graph that corresponds with what's shown in
the Preview Datatable Component.
'''
# NOTE: - Function for Graph Plot and Related Components
# TODO - Add Styling and Seperators
def graph(fig, feature_dropdown_option, securities_dropdown_option):
        return html.Div([

            html.H3(FEATURE_NAME_TO_PLOT),

            dcc.Dropdown(
                id='feature',
                options=[{'label': option, 'value': option} for option in feature_dropdown_option],
                value=DEFAULT_FEATURE,
                placeholder=FEATURE_DROPDOWN_PLACEHOLDER,
                searchable=False,
                clearable=False,
                style=dropdown_style,
            ),

            html.H3(SECURITIES_TO_DISPLAY),

            dcc.Dropdown(
                id='securities',
                options=[{'label': option, 'value': option} for option in securities_dropdown_option],
                value=[DEFAULT_STOCK],
                # TODO: Convert to Constant String
                placeholder=STOCK_DROPDOWN_PLACEHOLDER,
                multi=True,
                searchable=False,
                clearable=False,
                style=dropdown_style,
            ),
            
            dcc.Graph(
                id='graph',
                figure=fig
            )
        ],
        style=center_div_contents
        )
# !SECTION


