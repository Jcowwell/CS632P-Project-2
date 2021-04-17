# NOTE - Constants
import dash_html_components as html

DATATYPES = [
    'String',
    'Integer',
    'Float',
    'Boolean',
    'Date'
]
COLUMN_NAMES = 'Column Names'
_DATATYPES = 'DataTypes'
STOCK = 'Stock'
PREVIEW_DROPDOWN_HEADER = 'Curve Identifier to Display'
FEATURE_NAME_TO_PLOT = 'Feature Name to Plot'
SECURITIES_TO_DISPLAY = 'Securities to Display'
DATE = 'DATE'
PAGE_SIZE = 15
ERROR_DIV = html.Div([
            'There was an error processing this file.'
            ]), html.Div()