
import dash_core_components as dcc
import dash_html_components as html
from styles import layout_style, hide_div, button_style, upload_style

# SECTION: - App Layout

# NOTE: - Dash-Layout component
layout = html.Div(
    [
        # SECTION: - Display Divs

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

        # !SECTION

        # SECTION: - Data Storing Divs

        # Hidden div that stores the intermediate value (in this case DataFrames)
        html.Div(id='dataframe-value', style=hide_div),

        # Hidden div that stores a JSON representation of a lists of Permtted Columns according to User input
        html.Div(id='permitted-columns', style=hide_div),

        # Hidden div that stores a JSON representation of a lists of Unique Stock Values according to User input
        html.Div(id='stock-values', style=hide_div),

        # Hidden div that stores a JSON representation of a lists of numerical datatype Columns according to User input
        html.Div(id='feature-values', style=hide_div)

        # !SECTION
    ], 

    style=layout_style
)