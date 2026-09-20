import pandas as pd
import pandas.api.types as ptypes

type_mapping = {
                    "string": "string",
                    "integer": "integer",
                    "boolean": "boolean",
                    "floating": "float",
                    "datetime64": "datetime",
                    "mixed": "unsupported_type",
               }

def get_missing_values(df: pd.DataFrame) -> dict:
    """
    Returns the number of missing values in each column of the given DataFrame as a dictionary.

    Parameters:
        df (pd.DataFrame): The DataFrame whose missing values are to be determined.
    Returns:
        dict: A dictionary where the keys are column names and the values are 
        the number of missing values in each column.    
    """
    return df.isna().sum().to_dict()

def get_duplicates(df: pd.DataFrame) -> dict :
    """
    Returns the number of duplicated rows as a dictionary.
       
    Parameters:
        df (pd.DataFrame): The DataFrame whose number of duplicated rows are to be determined.
    Returns:
        dict: A dictionary that shows the number of duplicated rows.
    """
    return {
        "duplicate_rows_count": df.duplicated().sum()
    }

def get_shape(df: pd.DataFrame) -> dict:
    """
    Returns the shape of the given DataFrame as a dictionary.

    Parameters:
        df (pd.DataFrame): The DataFrame whose shape is to be determined.
    Returns:
        dict: A dictionary containing the number of rows and columns in the DataFrame.
    """
    rows, columns = df.shape
    return {
        "rows": rows,
        "columns": columns,
        }

def get_quality(df: pd.DataFrame) -> dict:
    """
    Returns a summary of the data quality characteristics of the given DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame whose quality is to be determined.
    Returns:
        dict: A dictionary containing the data quality information, including missing values and duplicated rows.
    """
    return {
        "missing_values": get_missing_values(df),
        "duplicates": get_duplicates(df)
    }

def get_data_types(df: pd.DataFrame) -> dict:    
    """
    Returns the data types of each column in the given DataFrame as a dictionary where the 
    keys are the column names and the values are the corresponding data types.

    Parameters:
        df (pd.DataFrame): The DataFrame whose data types are to be determined.

    Returns:
        dict: A dictionary where the keys are column names and the values are the corresponding data types.
    """
    return {
        column: str(dtype) for column, dtype in df.dtypes.items()
    }

def get_generic_data_type(column: pd.Series) -> str:

    """ 
    Infers the generic data type of a pandas Series. 
    The function classifies the column as a generic type used by the validation layer,
      such as string, integer, float, boolean, datetime, mixed, all_null, empty, or unsupported_type. 

    Parameters: 

        column (pd.Series): The column to classify. 

    Returns: 

        str: The inferred generic data type of the column. 
    """
    column_type = ptypes.infer_dtype(column, skipna=True)
    if column.empty:
            return "empty"
    if column.isnull().all():
            return "all_null"
    if column_type.startswith("mixed-"):
          return "mixed"
    return type_mapping.get(column_type, "unsupported_type")      

def get_unique_values_count(df: pd.DataFrame) -> dict:   
    """
    Returns the number of unique values in each column of the given DataFrame as a dictionary.

    Parameters:
        df (pd.DataFrame): The DataFrame whose unique values are to be determined.
    Returns:
        dict: A dictionary where the keys are column names and the values are the number of unique values in each column.
    """
    return {
        column: df[column].nunique(dropna=True) for column in df.columns
    }

def get_numeric_statistics(df: pd.DataFrame) -> dict:
    """
    Returns numeric statistics for each numeric column in the DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame for which numeric statistics
            will be calculated.

    Returns:
        dict: A dictionary containing statistics for each numeric column.
            If no numeric columns are found, the statistics dictionary is empty.
    """
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return {
            "statistics": {},
            "message": "No numeric columns found."
        }

    statistics = (
        numeric_df.describe()
        .T
        .rename(columns={
            "25%": "q1",
            "50%": "median",
            "75%": "q3"
        })
        .to_dict(orient="index")
    )

    return {
        "statistics": statistics,
        "message": None
    }
    
def profile_data(df: pd.DataFrame) -> dict:
   
   """
   Profiles the given DataFrame and returns a summary of its characteristics.

   Parameters:
        df (pd.DataFrame): The DataFrame to be profiled.
   Returns:  
        dict: A dictionary containing:
            - "shape": The number of rows and columns.
            - "data_types": The data type of each column.
            - "unique_values_count": The number of unique values in each column.
            - "numeric_statistics": Numeric statistics for each numeric column.
            - "quality": Information about missing values and duplicate rows. 
   """
   return {
    "shape": get_shape(df),
    "pandas_types": get_data_types(df),
    "generic_types": { column:get_generic_data_type(df[column]) for column in df},
    "unique_values_count": get_unique_values_count(df),
    "numeric_statistics": get_numeric_statistics(df),
    "quality": get_quality(df),
   }
    

