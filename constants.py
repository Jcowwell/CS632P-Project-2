# NOTE - Constants
import dash_html_components as html

DATATYPES = [
    'String',
    'Integer',
    'Float',
    'Boolean',
    'Date'
]
# NOTE: - DATAFRAME CONSTANTS
STOCK = 'Stock'
DATE = 'Date'
ADJ_CLOSE = 'Adj Close'
PAGE_SIZE = 15
# NOTE: - DEFAULT OPTIONS CONSTANTS 
DEFAULT_FEATURE = 'Adj Close'
DEFAULT_STOCK = 'AAPL'
# NOTE: - TITLE STRING CONSTANTS
PREVIEW_DROPDOWN_HEADER = 'Curve Identifier to Display'
FEATURE_NAME_TO_PLOT = 'Feature Name to Plot'
SECURITIES_TO_DISPLAY = 'Securities to Display'
FEATURE_DROPDOWN_PLACEHOLDER = "Select a Feature to Plot"
STOCK_DROPDOWN_PLACEHOLDER = "Select a Stock to Display"
#NOTE: -  DASH HTML CONSTANTS
ERROR_DIV = html.Div([
            'There was an error processing this file.'
            ]), html.Div()
# NOTE: - MISC
COLUMN_NAMES = 'Column Names'
DATATYPES_ = 'DataTypes'