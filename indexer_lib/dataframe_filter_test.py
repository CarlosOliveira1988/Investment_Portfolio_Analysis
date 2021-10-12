"""This file is used to test the 'dataframe_filter.py'."""

from datetime import datetime

import pandas as pd
import pytest

from indexer_lib.dataframe_filter import DataframeFilter

"""Tuple objects for testing purpose: dataframe + filter."""


def getTestObjects():
    """Return a dataframe and a DataframeFilter objects for testing purpose."""
    table_dict = {
        "col1": range(6),
        "col2": range(6, 12),
        "date": pd.date_range(start="2021-10-01", end="2021-10-06").tolist(),
    }
    return pd.DataFrame(data=table_dict), DataframeFilter()


def fullTestDataframe():
    """Return a full test dataframe."""
    df, filter = getTestObjects()
    return df, filter


def nonCol1TestDataframe():
    """Return a non-Col1 test dataframe."""
    df, filter = getTestObjects()
    df.drop(["col1"], axis="columns", inplace=True)
    return df, filter


def nonCol2TestDataframe():
    """Return a non-Col2 test dataframe."""
    df, filter = getTestObjects()
    df.drop(["col2"], axis="columns", inplace=True)
    return df, filter


def nonDateTestDataframe():
    """Return a non-Date test dataframe."""
    df, filter = getTestObjects()
    df.drop(["date"], axis="columns", inplace=True)
    return df, filter


def emptyTestDataframe():
    """Return a empty test dataframe."""
    df, filter = getTestObjects()
    df.drop(["col1", "col2", "date"], axis="columns", inplace=True)
    return df, filter


def nonDataframe():
    """Return a non-dataframe type."""
    df, filter = getTestObjects()
    df = int()
    return df, filter


"""Tests for 'filterDataframePerColumn' method."""


filterDataframePerColumn_list = [
    fullTestDataframe(),
    nonCol1TestDataframe(),
    nonCol2TestDataframe(),
    nonDateTestDataframe(),
    emptyTestDataframe(),
]


@pytest.mark.parametrize("dft, filter", filterDataframePerColumn_list)
def test_filterDataframePerColumn_validValues(dft, filter):
    """Test the 'filterDataframePerColumn' method against dataframes.

    The application will not brake if some column is not found.
    """
    fdf = filter.filterDataframePerColumn(dft, "col1", 0)
    assert isinstance(fdf, pd.DataFrame) is True


def test_filterDataframePerColumn_nonValidValues():
    """Test the 'filterDataframePerColumn' method against non-dataframes.

    An exception will be raised if non-dataframe type is used.
    """
    non_dft, filter = nonDataframe()
    with pytest.raises(TypeError):
        fdf = filter.filterDataframePerColumn(non_dft, "col1", 0)


def test_filterDataframePerColumn_foundOK():
    """Check if the filter works correctly with one valid value."""
    dft, filter = fullTestDataframe()
    fdf = filter.filterDataframePerColumn(dft, "col1", 0)
    assert len(fdf) == 1


def test_filterDataframePerColumn_foundNOK():
    """Check if the filter works correctly when none valid value is found."""
    dft, filter = fullTestDataframe()
    fdf = filter.filterDataframePerColumn(dft, "col1", 1000)
    assert len(fdf) == 0


"""Tests for 'filterDataframePerPeriod' method."""

lower_invalid_date = datetime.strptime("2020/10/01", "%Y/%m/%d")
initial_date = datetime.strptime("2021/10/01", "%Y/%m/%d")
medium_date = datetime.strptime("2021/10/04", "%Y/%m/%d")
final_date = datetime.strptime("2021/10/06", "%Y/%m/%d")
upper_invalid_date = datetime.strptime("2022/10/06", "%Y/%m/%d")

filterDataframePerPeriod_list = [
    fullTestDataframe() + (initial_date, final_date),
    nonCol1TestDataframe() + (initial_date, final_date),
    nonCol2TestDataframe() + (initial_date, final_date),
    nonDateTestDataframe() + (initial_date, final_date),
    emptyTestDataframe() + (initial_date, final_date),
]


@pytest.mark.parametrize(
    "dft, filter, ini_date, end_date", filterDataframePerPeriod_list
)
def test_filterDataframePerPeriod_validValues(dft, filter, ini_date, end_date):
    """Test the 'filterDataframePerPeriod' method against dataframes.

    The application will not brake if some column is not found.
    """
    fdf = filter.filterDataframePerPeriod(
        dft,
        "date",
        ini_date,
        end_date,
    )
    assert isinstance(fdf, pd.DataFrame) is True


def test_filterDataframePerPeriod_nonValidValues():
    """Test the 'filterDataframePerPeriod' method against non-dataframes.

    An exception will be raised if non-dataframe type is used.
    """
    non_dft, filter = nonDataframe()
    ini_date = initial_date
    end_date = final_date
    with pytest.raises(TypeError):
        fdf = filter.filterDataframePerPeriod(
            non_dft,
            "date",
            ini_date,
            end_date,
        )


filterDataframePerPeriod_dateList = [
    (initial_date, final_date, 6),
    (initial_date, medium_date, 4),
    (medium_date, final_date, 3),
    (lower_invalid_date, upper_invalid_date, 6),
    (upper_invalid_date, lower_invalid_date, 0),
]


@pytest.mark.parametrize(
    "ini_date, end_date, expected_len", filterDataframePerPeriod_dateList
)
def test_filterDataframePerPeriod_foundOK(ini_date, end_date, expected_len):
    """Check if the filter works correctly with some valid interval."""
    dft, filter = fullTestDataframe()
    fdf = filter.filterDataframePerPeriod(dft, "date", ini_date, end_date)
    assert len(fdf) == expected_len


"""Tests for 'getListFromDataframeColumn' method."""

getListFromDataframeColumn_list = [
    fullTestDataframe(),
    nonCol1TestDataframe(),
    nonCol2TestDataframe(),
    nonDateTestDataframe(),
    emptyTestDataframe(),
]


@pytest.mark.parametrize("dft, filter", getListFromDataframeColumn_list)
def test_getListFromDataframeColumn_validValues(dft, filter):
    """Test the 'getListFromDataframeColumn' method against dataframes.

    The application will not brake if some column is not found.
    """
    result_list = filter.getListFromDataframeColumn(dft, "col1")
    assert isinstance(result_list, list) is True


def test_getListFromDataframeColumn_nonValidValues():
    """Test the 'getListFromDataframeColumn' method against non-dataframes.

    An exception will be raised if non-dataframe type is used.
    """
    non_dft, filter = nonDataframe()
    with pytest.raises(TypeError):
        fdf = filter.getListFromDataframeColumn(non_dft, "col1")


def test_getListFromDataframeColumn_foundOK():
    """Check if the filter works correctly with some valid values."""
    dft, filter = fullTestDataframe()
    fdf = filter.getListFromDataframeColumn(dft, "col1")
    assert len(fdf) == 6
