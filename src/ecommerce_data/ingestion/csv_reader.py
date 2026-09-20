import pandas as pd
from pathlib import Path

def read_csv(file_path: Path | str) -> pd.DataFrame:
    """Read a csv file and return pandas DataFrame."""
    
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist")
    else:
       return pd.read_csv(file_path)