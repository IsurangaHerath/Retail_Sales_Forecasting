"""Locate, load and inspect the Kaggle *Store Sales* dataset.

The dataset must be downloaded manually from Kaggle and placed in
``data/raw/``. This module never downloads data and never fabricates it:
it only reads CSV files that already exist on disk.

Why this module exists
----------------------
Keeping file discovery and schema inspection in one reusable place means the
notebook and the tests share exactly the same logic. It also makes the
"is the dataset present?" check explicit instead of scattering ``read_csv``
calls across notebooks.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

# Folder that holds the raw Kaggle CSVs, relative to the repository root.
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# Logical name -> expected filename on disk.
EXPECTED_FILES: Dict[str, str] = {
    "train": "train.csv",
    "test": "test.csv",
    "stores": "stores.csv",
    "transactions": "transactions.csv",
    "oil": "oil.csv",
    "holidays": "holidays_events.csv",
}

# Files without which the project cannot proceed.
REQUIRED_FILES: tuple[str, ...] = ("train", "test", "stores")


class DatasetNotFoundError(FileNotFoundError):
    """Raised when an expected Kaggle CSV is missing from ``data/raw/``."""


def resolve_raw_dir(raw_dir: Optional[str | Path] = None) -> Path:
    """Return the directory that holds the raw CSVs.

    Parameters
    ----------
    raw_dir:
        Optional override, mainly useful in tests. When ``None`` the default
        ``data/raw`` folder next to this package is used.
    """
    return Path(raw_dir) if raw_dir is not None else RAW_DIR


def available_files(raw_dir: Optional[str | Path] = None) -> Dict[str, Path]:
    """Return ``{logical_name: path}`` for every expected file that exists."""
    base = resolve_raw_dir(raw_dir)
    return {
        key: base / filename
        for key, filename in EXPECTED_FILES.items()
        if (base / filename).exists()
    }


def missing_files(raw_dir: Optional[str | Path] = None) -> List[str]:
    """Return the filenames of expected CSVs that are not present on disk."""
    base = resolve_raw_dir(raw_dir)
    return [
        filename
        for filename in EXPECTED_FILES.values()
        if not (base / filename).exists()
    ]


def require_dataset(raw_dir: Optional[str | Path] = None) -> None:
    """Raise a helpful error if a *required* file is missing.

    This keeps the failure message actionable (it tells the user exactly what
    to download and where to put it) instead of a bare ``FileNotFoundError``.
    """
    base = resolve_raw_dir(raw_dir)
    missing_required = [
        EXPECTED_FILES[key]
        for key in REQUIRED_FILES
        if not (base / EXPECTED_FILES[key]).exists()
    ]
    if missing_required:
        missing_text = ", ".join(missing_required)
        raise DatasetNotFoundError(
            f"Missing required dataset file(s): {missing_text}. "
            f"Download the Kaggle 'Store Sales - Time Series Forecasting' "
            f"competition data and place the CSV files in '{base}'."
        )


def load_csv(
    key: str,
    raw_dir: Optional[str | Path] = None,
    **read_csv_kwargs,
) -> pd.DataFrame:
    """Load one dataset CSV by its logical name (e.g. ``"train"``)."""
    if key not in EXPECTED_FILES:
        valid = ", ".join(sorted(EXPECTED_FILES))
        raise KeyError(f"Unknown dataset key '{key}'. Expected one of: {valid}")

    base = resolve_raw_dir(raw_dir)
    path = base / EXPECTED_FILES[key]
    if not path.exists():
        raise DatasetNotFoundError(
            f"Expected file not found: '{path}'. "
            f"Download the Kaggle competition data into '{base}'."
        )
    return pd.read_csv(path, **read_csv_kwargs)


def load_dataset(raw_dir: Optional[str | Path] = None) -> Dict[str, pd.DataFrame]:
    """Load every expected CSV that is present and return them by logical name.

    Missing *optional* files are simply omitted from the result. Missing
    *required* files raise :class:`DatasetNotFoundError` via
    :func:`require_dataset`.
    """
    require_dataset(raw_dir)
    return {
        key: load_csv(key, raw_dir=raw_dir)
        for key in available_files(raw_dir)
    }


def inspect_dataframe(df: pd.DataFrame, name: str = "dataframe") -> dict:
    """Return a plain-dict summary of a DataFrame's shape and quality."""
    return {
        "name": name,
        "rows": int(len(df)),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": {col: int(count) for col, count in df.isna().sum().items()},
        "duplicate_rows": int(df.duplicated().sum()),
    }


def inspect_sales_dates(
    train_df: pd.DataFrame,
    date_col: str = "date",
) -> dict:
    """Summarise the temporal coverage of the training data.

    Returns the first/last date, the number of calendar days covered and how
    many unique dates actually appear. Comparing ``n_days`` with
    ``n_unique_dates`` is an early warning for missing calendar dates.
    """
    if date_col not in train_df.columns:
        raise KeyError(f"Column '{date_col}' not found in training data.")

    dates = pd.to_datetime(train_df[date_col])
    first = dates.min()
    last = dates.max()
    return {
        "min_date": first.date().isoformat(),
        "max_date": last.date().isoformat(),
        "n_days": int((last - first).days + 1),
        "n_unique_dates": int(dates.nunique()),
    }


def summarise_dataset(raw_dir: Optional[str | Path] = None) -> dict:
    """Inspect every available CSV and return a combined summary dictionary.

    This is the single entry point used by the inspection script / notebook.
    """
    frames = load_dataset(raw_dir)
    summary: dict = {
        "raw_dir": str(resolve_raw_dir(raw_dir)),
        "available_files": sorted(frames),
        "missing_files": missing_files(raw_dir),
        "tables": {},
    }
    for key, df in frames.items():
        summary["tables"][key] = inspect_dataframe(df, name=key)

    if "train" in frames:
        summary["train_dates"] = inspect_sales_dates(frames["train"])

    return summary


def main() -> None:
    """Print a human-readable summary of the raw dataset.

    Run with::

        python -m src.data_loader
    """
    import sys

    try:
        summary = summarise_dataset()
    except DatasetNotFoundError as exc:
        print(f"Dataset not ready: {exc}", file=sys.stderr)
        print(
            "See docs/DATASET.md for download instructions.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    print(f"Raw data directory: {summary['raw_dir']}")
    print(f"Available files:    {', '.join(summary['available_files']) or 'none'}")
    print(f"Missing files:      {', '.join(summary['missing_files']) or 'none'}")
    for name, table in summary["tables"].items():
        print(f"\n[{name}] rows={table['rows']} cols={len(table['columns'])}")
        print(f"  columns: {table['columns']}")
        print(f"  duplicate rows: {table['duplicate_rows']}")
        missing = {k: v for k, v in table["missing_values"].items() if v}
        print(f"  columns with missing values: {missing or 'none'}")
    if "train_dates" in summary:
        d = summary["train_dates"]
        print(
            f"\nTrain dates: {d['min_date']} to {d['max_date']} "
            f"({d['n_days']} calendar days, {d['n_unique_dates']} unique dates)"
        )


if __name__ == "__main__":
    main()
