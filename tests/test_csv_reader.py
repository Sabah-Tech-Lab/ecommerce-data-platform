"""Tests for CSV ingestion using the project read_csv helper."""

import pandas as pd
import pytest
from ecommerce_data.ingestion.csv_reader import read_csv

    # ------------------------------------------------------------------
    # Fixtures to use as path
    # ------------------------------------------------------------------
@pytest.fixture
def csv_file(tmp_path):
    """Create a temporary CSV file for ingestion tests."""
    csv_file = tmp_path/"test.csv"
    csv_file.write_text(
        "name,age\n"
        "Alice,30\n"
        "Bob,32\n"
    )
    return csv_file

   # ------------------------------------------------------------------
    # Test read_csv() function.
    # ------------------------------------------------------------------

def test_read_csv_with_path(csv_file):
    
    result = read_csv(csv_file)
    expected_result = pd.DataFrame(
        {
            "name": ["Alice","Bob"],
            "age": [30,32]
        }
    )
    pd.testing.assert_frame_equal(result, expected_result)

def test_read_csv_with_string(csv_file):
    
    result = read_csv(str(csv_file))
    expected_result = pd.DataFrame(
        {
            "name": ["Alice","Bob"],
            "age": [30,32]
        }
    )
    pd.testing.assert_frame_equal(result, expected_result)    