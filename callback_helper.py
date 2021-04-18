import io
import pandas as pd
import base64

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
Process Non-Ignored Data and return a Div Object consiting of a Datatable.
'''
def process_data(permitted_data, dataframe_json):
    dataframe = pd.read_json(dataframe_json, orient='split')
    columns = [column['Column Names'] for column in permitted_data] 
    _dataypes = [__datatypes['DataTypes'] for __datatypes in permitted_data]

    # FIXME: - Convert Column Data to DataType based on Index. Perhaps use a Function. 
    return dataframe[columns]

def get_numerical_columns(dataframe):
    # TODO: Filter Dataframe by getting only Columns that have Int and Float values. 
    return


