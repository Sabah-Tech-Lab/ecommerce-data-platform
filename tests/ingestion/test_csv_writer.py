from pathlib import Path

import pandas as pd
import pytest

from ecommerce_data.ingestion.csv_writer import write_csv

# ------------------------------------------------------------------
# Fixtures for write_csv()
# ------------------------------------------------------------------

@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["A", "B"],
        }
    )

# ------------------------------------------------------------------
# tests for write_csv()
# ------------------------------------------------------------------

def test_write_csv_creates_file(
        tmp_path: Path, 
        sample_dataframe: pd.DataFrame,
) -> None:
    """Verify that write_csv creates a csv file at the given path."""
    output_path = tmp_path / "test.csv"

    write_csv(sample_dataframe, output_path)

    assert output_path.exists()

def test_write_csv_preserves_data(
        tmp_path: Path,
        sample_dataframe: pd.DataFrame,
) -> None:
    """"Verify that write_csv preserves the DataFrame contents. """
    output_path = tmp_path / "test.csv"

    write_csv(sample_dataframe, output_path)

    written_df = pd.read_csv(output_path)

    pd.testing.assert_frame_equal(
        written_df,
        sample_dataframe,
    )