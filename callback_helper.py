import io
import base64
import numpy as np
import pandas as pd

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
Returns a Dataframe from a JSON Object
'''
def unload_dataframe(dataframe_json):
    return pd.read_json(dataframe_json, orient='split')

''' 
NOTE: -
Process Non-Ignored Data and return a Div Object consiting of a Datatable.
'''
def filter_dataframe(permitted_data, dataframe):
    columns = [column['Column Names'] for column in permitted_data] 
    _dataypes = [__datatypes['DataTypes'] for __datatypes in permitted_data]

    # FIXME: - Convert Column Data to DataType based on Index. Perhaps use a Function. 
    return dataframe[columns]

''' 
NOTE: -
Returns a lists of Column Names that consists of numerical values
'''
def get_numerical_columns(dataframe):
    # TODO: Filter Dataframe by getting only Columns that have Int and Float values.
    if dataframe is not None:
        return dataframe.select_dtypes(include=np.number).columns.tolist()
    return []

''' 
NOTE: -
Returns a lists of Unique Values from desired DataFrame Column.
'''
def get_unique_values(dataframe, column_name):
    if dataframe is not None or column_name is not None:
        try:
            return dataframe[column_name].unique().tolist()
        except Exception as e:
            print(e)
    return []



