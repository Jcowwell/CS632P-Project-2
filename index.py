from app import app
from layout import layout
# NOTE: - All callbacks must be defined before the server starts.
import callbacks

app.layout = layout

if __name__ == '__main__':
    # SECTION: - Launch Application
    # NOTE: - Launch Application in Debugger Mode
    app.run_server(debug=True)
    # NOTE: - Launch Application in Normal Mode
    # app.run_server()
    # !SECTION