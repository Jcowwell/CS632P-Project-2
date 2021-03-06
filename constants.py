# NOTE - Constants
import dash_html_components as html
import numpy as np

DATATYPES = [
    'String',
    'Integer',
    'Float',
    'Boolean',
    'Date'
]

DATATYPE_MAP = {
    'String': "str",
    'Integer': "int",
    'Float': "float",
    'Date': "np.datetime64",
}
DATATYPES_CONVERSION_OPTIONS = {
    'object':['String'],
    'float64':['String', 'Integer'],
    'int64':['String', 'Float'],
    'datetime64[ns]':['Date']
}

# NOTE: - DATAFRAME CONSTANTS
STOCK = 'Stock'
DATE = 'Date'
ADJ_CLOSE = 'Adj Close'
VOLUME = 'Volume'
EXCHANGE = 'Exchange'
PAGE_SIZE = 15
# NOTE: - DEFAULT OPTIONS CONSTANTS 
DEFAULT_FEATURE = 'Adj Close'
DEFAULT_STOCK = 'AAPL'
# NOTE: - TITLE STRING CONSTANTS
FILTER_TABLE_TITLE = 'Filter Table'
PREVIEW_DROPDOWN_HEADER = 'Curve Identifier to Display'
FEATURE_NAME_TO_PLOT = 'Feature Name to Plot'
SECURITIES_TO_DISPLAY = 'Securities to Display'
FEATURE_DROPDOWN_PLACEHOLDER = "Select a Feature to Plot"
STOCK_DROPDOWN_PLACEHOLDER = "Select a Stock to Display"
#NOTE: -  DASH HTML CONSTANTS
ERROR_DIV = html.Div([
            'There was an error processing this file.'
            ])
EMPTY_DIV = html.Div()
# NOTE: - MISC
COLUMN_NAMES = 'Column Names'
DATATYPES_ = 'DataTypes'