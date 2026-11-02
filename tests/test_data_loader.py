"""Tests for :mod:`src.data_loader`.

These use tiny synthetic CSV files written to a temporary directory, so they
run fast and never depend on the real Kaggle download.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.data_loader import (
    DatasetNotFoundError,
    available_files,
    inspect_dataframe,
    inspect_sales_dates,
    load_csv,
    load_dataset,
    missing_files,
    require_dataset,
    summarise_dataset,
)


def _write_minimal_dataset(base: Path) -> None:
    """Write a tiny but structurally realistic dataset to ``base``."""
    train = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "date": ["2020-01-01", "2020-01-01", "2020-01-02", "2020-01-02"],
            "store_nbr": [1, 2, 1, 2],
            "family": ["A", "A", "A", "A"],
            "sales": [10.0, 5.0, 12.0, 6.0],
            "onpromotion": [0, 1, 0, 0],
        }
    )
    test = train.copy()
    test["date"] = ["2020-01-03", "2020-01-03", "2020-01-04", "2020-01-04"]
    test["sales"] = [0.0, 0.0, 0.0, 0.0]
    stores = pd.DataFrame({"store_nbr": [1, 2], "city": ["X", "Y"], "type": ["A", "B"]})

    train.to_csv(base / "train.csv", index=False)
    test.to_csv(base / "test.csv", index=False)
    stores.to_csv(base / "stores.csv", index=False)


def test_available_files_detects_present_files(tmp_path: Path) -> None:
    _write_minimal_dataset(tmp_path)
    found = available_files(tmp_path)
    assert set(found) == {"train", "test", "stores"}


def test_missing_files_lists_absent_files(tmp_path: Path) -> None:
    _write_minimal_dataset(tmp_path)
    missing = missing_files(tmp_path)
    assert "transactions.csv" in missing
    assert "oil.csv" in missing
    assert "holidays_events.csv" in missing
    assert "train.csv" not in missing


def test_load_csv_raises_for_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DatasetNotFoundError):
        load_csv("oil", raw_dir=tmp_path)


def test_load_csv_rejects_unknown_key(tmp_path: Path) -> None:
    with pytest.raises(KeyError):
        load_csv("does_not_exist", raw_dir=tmp_path)


def test_require_dataset_passes_when_required_present(tmp_path: Path) -> None:
    _write_minimal_dataset(tmp_path)
    require_dataset(tmp_path)  # should not raise


def test_require_dataset_raises_when_required_missing(tmp_path: Path) -> None:
    with pytest.raises(DatasetNotFoundError):
        require_dataset(tmp_path)


def test_load_dataset_returns_only_present_tables(tmp_path: Path) -> None:
    _write_minimal_dataset(tmp_path)
    frames = load_dataset(tmp_path)
    assert set(frames) == {"train", "test", "stores"}
    assert len(frames["train"]) == 4


def test_inspect_dataframe_reports_shape_and_quality() -> None:
    # Row 2 and row 3 are identical, so there is exactly one duplicate row.
    df = pd.DataFrame({"a": [1, 2, 2], "b": [None, "x", "x"]})
    info = inspect_dataframe(df, name="demo")
    assert info["name"] == "demo"
    assert info["rows"] == 3
    assert info["columns"] == ["a", "b"]
    assert info["duplicate_rows"] == 1
    assert info["missing_values"]["b"] == 1


def test_inspect_sales_dates_reports_coverage(tmp_path: Path) -> None:
    train = pd.DataFrame(
        {"date": ["2020-01-01", "2020-01-01", "2020-01-03"]}
    )
    info = inspect_sales_dates(train)
    assert info["min_date"] == "2020-01-01"
    assert info["max_date"] == "2020-01-03"
    assert info["n_days"] == 3
    # 2020-01-02 is absent, so only two unique dates exist.
    assert info["n_unique_dates"] == 2


def test_summarise_dataset_combines_tables(tmp_path: Path) -> None:
    _write_minimal_dataset(tmp_path)
    summary = summarise_dataset(tmp_path)
    assert set(summary["tables"]) == {"train", "test", "stores"}
    assert summary["train_dates"]["min_date"] == "2020-01-01"
    assert summary["train_dates"]["max_date"] == "2020-01-02"
