from constants import DATATYPES_CONVERSION_OPTIONS, PAGE_SIZE
import io
import base64
import numpy as np
import pandas as pd

# SECTION: - Callback Function Helpers

''' 
NOTE: - Adopted from: https://dash.plotly.com/dash-core-components/upload
Processes CSV and XLS Content Data
'''
def process_file(contents, filename):
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
Returns a JSON Object from a Dataframe
'''
def dump_dataframe(dataframe):
    return dataframe.to_json(date_format='iso', orient='split')

''' 
NOTE: -
Returns a Dataframe from a JSON Object
'''
def load_dataframe(dataframe_json):
    return pd.read_json(dataframe_json, orient='split')

''' 
NOTE: -
Returns a Dataframe Object filtered by permitted a column and value.
'''
def filter_dataframe_by_column_value(dataframe, column, value):
    if column not in dataframe.columns:
        return dataframe
    # Create Series Object to filter for wanted value in column
    is_value = dataframe[column].isin(value)
    # Use Series to filter Dataframe
    return dataframe[is_value]

''' 
NOTE: -
Returns a Dataframe Object with permitted column(s).
'''
def filter_dataframe_columns(dataframe, permitted_columns):
    columns = [column['Column Names'] for column in permitted_columns] 
    _dataypes = [__datatypes['DataTypes'] for __datatypes in permitted_columns]

    # FIXME: - Convert Column Data to DataType based on Index. Perhaps use a Function. 
    return dataframe[columns]

''' 
NOTE: -
Returns a Dict of Column Name Dataypes
'''
def get_dataframe_column_datatype(dataframe):
    if dataframe is not None and 'Date' in dataframe.columns:
            dataframe['Date'] =  dataframe['Date'].astype('datetime64[ns]')
            return {column: DATATYPES_CONVERSION_OPTIONS[datatype.name] for column, datatype in dataframe.dtypes.to_dict().items()}
    return {}

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
Returns a Dataframe with proper Date Dataype for future Column Datatype Options
'''
def datify_dataframe(dataframe):
    # TODO: Filter Dataframe by getting only Columns that have Int and Float values.
    if dataframe is not None and 'Date' in dataframe.columns:
            dataframe['Date'] =  dataframe['Date'].astype('datetime64[ns]')
    return dataframe

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

''' 
NOTE: -
Returns a Paginate Dataframe
'''
def paginate(dataframe, page_current=0, page_size=0):
    return dataframe.iloc[page_current*page_size:(page_current+ 1)*page_size]
