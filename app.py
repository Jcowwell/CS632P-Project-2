import dash
from styles import app_style

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.css.append_css(app_style)
server = app.server