import dash
from styles import app_style

# NOTE: - There are Callbacks that use Components that are not generated yet so we call this to supress Callback Exceptions
app = dash.Dash(__name__, suppress_callback_exceptions=True)
# Append Style for the entire application
app.css.append_css(app_style)
# 
server = app.server