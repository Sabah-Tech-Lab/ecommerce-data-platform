"""Unit tests for the reusable data-profiling helpers."""

import pandas as pd
import pytest
from ecommerce_data.profiling.data_profiler import get_missing_values, get_duplicates, get_quality, get_shape, profile_data, get_data_types, get_unique_values_count, get_numeric_statistics, get_generic_data_type

#Defining Fixtures

@pytest.fixture
def data_with_missing_and_duplicates():
    """Return sample data containing both missing values and duplicate rows."""
    return pd.DataFrame({
        'name': ['Alice', 'Alice', 'Charlie', None, 'Eve'],
        'age': pd.Series([25, 25, 35, 40, None],dtype="Int64"),
        'city': ['New York', 'New York', 'Chicago', 'Houston', 'Phoenix']
        })
                                      
@pytest.fixture
def data_without_missing_or_duplicates():
    """Return clean sample data without missing values or duplicate rows.""" 
    return pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'Los Angeles', 'Chicago']
        }) 

@pytest.fixture
def data_types():
    """Return sample columns covering common pandas data types."""
    return pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25,30,35],
        'price': [19.99, 29.99, 39.99],
        'created_at': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03'])
       })

@pytest.fixture
def data_without_numeric_values():
    """Return sample data containing no numeric columns."""
    return pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'created_at': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03'])
           })

@pytest.fixture
def dataframe_type_samples():
   """Return representative columns used to test generic type inference."""
   type_samples = pd.DataFrame({
        "string": ["Alice", "Bob"],
        "integer": [25, 30],
        "float": [99.56, 57.69],
        "boolean": [True, False],
        "datetime": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "mixed": ["Alice", 25],
        "all_null": [None, None],
        "integer_and_null": pd.Series([20, None], dtype="Int64"),
        "unsupported_type":[{"color":"green"},{"weight":50}],

        })
   type_samples["empty"] = pd.Series([])
   return type_samples

@pytest.fixture
def empty_column():
    """Return an empty object-dtype Series for generic type detection."""
    return pd.Series([], dtype="object")

#Testing get_missing_values function

def test_get_missing_values(data_with_missing_and_duplicates):
    
    expected_result = {
        'name': 1, 'age': 1, 'city':0
        }
    result = get_missing_values(data_with_missing_and_duplicates)
    assert result == expected_result 

def test_get_missing_values_no_missing(data_without_missing_or_duplicates):
    expected_result = {
        'name': 0, 'age': 0, 'city':0
        }
    result = get_missing_values(data_without_missing_or_duplicates)
    assert result == expected_result 

#Testing get_duplicates function

def test_get_duplicates(data_with_missing_and_duplicates):
    expected_result = {
        'duplicate_rows_count': 1
        }
    result = get_duplicates(data_with_missing_and_duplicates)
    assert result == expected_result 

def test_get_duplicates_no_duplicates(data_without_missing_or_duplicates):
    expected_result = {
        'duplicate_rows_count': 0
        }
    result = get_duplicates(data_without_missing_or_duplicates)
    assert result == expected_result 

#Testing get_quality function

def test_get_quality(data_with_missing_and_duplicates):    
    expected_result = {
        'missing_values': {'name': 1, 'age': 1, 'city': 0},
        'duplicates': {'duplicate_rows_count': 1}
    }   
    result = get_quality(data_with_missing_and_duplicates)  
    assert result == expected_result

#Testing get_shape function    

def test_get_shape(data_without_missing_or_duplicates):
    expected_result = {
        'rows': 3,
        'columns': 3
    }
    result = get_shape(data_without_missing_or_duplicates)  
    assert result == expected_result

#Testing get_data_types function    

def test_get_data_types(data_types):
    expected_result = {
        'name': 'object',
        'age': 'int64',
        'price': 'float64',
        'created_at': 'datetime64[ns]'
    }

    result = get_data_types(data_types)
    assert result == expected_result

#Testing get_generic_data_types function    

def test_get_generic_data_type_string(dataframe_type_samples):  
    expected_result = "string"
    result = get_generic_data_type(dataframe_type_samples["string"])
    assert result == expected_result  

def test_get_generic_data_type_integer(dataframe_type_samples):  
    expected_result = "integer"
    result = get_generic_data_type(dataframe_type_samples["integer"])
    assert result == expected_result   

def test_get_generic_data_type_float(dataframe_type_samples):  
    expected_result = "float"
    result = get_generic_data_type(dataframe_type_samples["float"])
    assert result == expected_result  

def test_get_generic_data_empty(empty_column):  
    expected_result = "empty"
    result = get_generic_data_type(empty_column)
    assert result == expected_result  

def test_get_generic_data_type_all_null(dataframe_type_samples):  
    expected_result = "all_null"
    result = get_generic_data_type(dataframe_type_samples["all_null"])
    assert result == expected_result             

def test_get_generic_data_type_boolean(dataframe_type_samples):  
    expected_result = "boolean"
    result = get_generic_data_type(dataframe_type_samples["boolean"])
    assert result == expected_result    

def test_get_generic_data_datetime(dataframe_type_samples):  
    expected_result = "datetime"
    result = get_generic_data_type(dataframe_type_samples["datetime"])
    assert result == expected_result      

def test_get_generic_data_mixed(dataframe_type_samples):  
    expected_result = "mixed"
    result = get_generic_data_type(dataframe_type_samples["mixed"])
    assert result == expected_result     

def test_get_generic_data_unsupported_type(dataframe_type_samples):  
    expected_result = "unsupported_type"
    result = get_generic_data_type(dataframe_type_samples["unsupported_type"])
    assert result == expected_result  

   
def test_get_generic_data_integer_and_null(dataframe_type_samples):  
    expected_result = "integer"
    result = get_generic_data_type(dataframe_type_samples["integer_and_null"])
    assert result == expected_result    

#Testing get_unique_values_count function    

def test_get_unique_values_count(data_with_missing_and_duplicates):
    expected_result = {
        'name': 3,  # Alice, Charlie, Eve
        'age': 3,   # 25, 35, 40
        'city': 4   # New York, Chicago, Houston, Phoenix
    }
    result = get_unique_values_count(data_with_missing_and_duplicates)
    assert result == expected_result

#Testing get_numeric_statistics function    

def test_get_numeric_statistics(data_without_missing_or_duplicates):
    expected_result ={
                       'statistics': {
                                      'age': {
                                          'count': 3.0, 
                                          'mean': 30.0, 
                                          'std': 5.0, 
                                          'min': 25.0, 
                                          'q1': 27.5, 
                                          'median': 30.0, 
                                          'q3': 32.5, 
                                          'max': 35.0
                                             }
                                     }, 
                       'message': None
                    }
    
    result = get_numeric_statistics(data_without_missing_or_duplicates)
    assert result == expected_result

def test_get_numeric_statistics_no_numeric_columns(data_without_numeric_values):
    expected_result = {
                       'statistics': {}, 
                       'message': 'No numeric columns found.'
                       }
    result = get_numeric_statistics(data_without_numeric_values)
    assert result == expected_result    

#Testing profile_data function

def test_profile_data(data_with_missing_and_duplicates):
    expected_result = {
        'shape': {'rows': 5, 'columns': 3},
        'pandas_types': { 'name': 'object', 'age': 'Int64', 'city': 'object'},
        'generic_types': { 'name': 'string', 'age': 'integer', 'city': 'string'},
        'unique_values_count': { 'name': 3, 'age': 3, 'city': 4},
        'numeric_statistics': {'statistics': {
                                             'age': {
                                                     'count': 4.0, 
                                                     'mean': 31.25, 
                                                     'std': 7.5, 
                                                     'min': 25.0, 
                                                     'q1': 25.0, 
                                                     'median': 30.0, 
                                                     'q3': 36.25, 
                                                     'max': 40.0
                                                     }
                                            }, 
                              'message': None},
        'quality': {
                'missing_values': {'name': 1, 'age': 1, 'city': 0},
                'duplicates': {'duplicate_rows_count': 1}
            }
    }
    result = profile_data(data_with_missing_and_duplicates)
    assert result == expected_result    


