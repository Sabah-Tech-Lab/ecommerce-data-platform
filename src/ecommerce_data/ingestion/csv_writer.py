from pathlib import Path

import pandas as pd


def write_csv(
    df: pd.DataFrame,
    file_path: Path | str,
) -> None:
    """Write a DataFrame to a CSV file."""
    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        file_path,
        index=False,
    )