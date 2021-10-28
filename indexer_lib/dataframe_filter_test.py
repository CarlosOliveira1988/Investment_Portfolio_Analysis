"""This file is used to test the 'dataframe_filter.py'."""

from datetime import datetime

import pandas as pd
import pytest

from indexer_lib.dataframe_filter import DataframeFilter


class ObjectsForTesting:
    """Tuple objects for testing purpose: dataframe + filter."""

    def getTestObjects(self):
        """Return a dataframe and a DataframeFilter for testing purpose."""
        start = "2021-10-01"
        end = "2021-10-06"
        table_dict = {
            "col1": range(6),
            "col2": range(6, 12),
            "date": pd.date_range(start=start, end=end).tolist(),
        }
        return pd.DataFrame(data=table_dict), DataframeFilter()

    def fullTestDataframe(self):
        """Return a full test dataframe."""
        df, filter = self.getTestObjects()
        return df, filter

    def nonCol1TestDataframe(self):
        """Return a non-Col1 test dataframe."""
        df, filter = self.getTestObjects()
        df.drop(["col1"], axis="columns", inplace=True)
        return df, filter

    def nonCol2TestDataframe(self):
        """Return a non-Col2 test dataframe."""
        df, filter = self.getTestObjects()
        df.drop(["col2"], axis="columns", inplace=True)
        return df, filter

    def nonDateTestDataframe(self):
        """Return a non-Date test dataframe."""
        df, filter = self.getTestObjects()
        df.drop(["date"], axis="columns", inplace=True)
        return df, filter

    def emptyTestDataframe(self):
        """Return a empty test dataframe."""
        df, filter = self.getTestObjects()
        df.drop(["col1", "col2", "date"], axis="columns", inplace=True)
        return df, filter

    def nonDataframe(self):
        """Return a non-dataframe type."""
        df, filter = self.getTestObjects()
        df = int()
        return df, filter


class Test_filterDataframePerColumn:
    """Tests for 'filterDataframePerColumn' method."""

    obj_for_testing = ObjectsForTesting()

    # List of tuples, with the following order per tuple:
    # - dft, filter
    validValues_list = [
        obj_for_testing.fullTestDataframe(),
        obj_for_testing.nonCol1TestDataframe(),
        obj_for_testing.nonCol2TestDataframe(),
        obj_for_testing.nonDateTestDataframe(),
        obj_for_testing.emptyTestDataframe(),
    ]

    @pytest.mark.parametrize("dft, filter", validValues_list)
    def test_validValues(self, dft, filter):
        """Test the 'filterDataframePerColumn' method against dataframes.

        The application will not brake if some column is not found.
        """
        fdf = filter.filterDataframePerColumn(dft, "col1", 0)
        assert isinstance(fdf, pd.DataFrame) is True

    def test_nonValidValues(self):
        """Test the 'filterDataframePerColumn' method against non-dataframes.

        An exception will be raised if non-dataframe type is used.
        """
        obj_for_testing = ObjectsForTesting()
        non_dft, filter = obj_for_testing.nonDataframe()
        with pytest.raises(TypeError):
            fdf = filter.filterDataframePerColumn(non_dft, "col1", 0)

    def test_foundOK(self):
        """Check if the filter works correctly with one valid value."""
        obj_for_testing = ObjectsForTesting()
        dft, filter = obj_for_testing.fullTestDataframe()
        fdf = filter.filterDataframePerColumn(dft, "col1", 0)
        assert len(fdf) == 1

    def test_foundNOK(self):
        """Check if the filter works correctly when no valid value is found."""
        obj_for_testing = ObjectsForTesting()
        dft, filter = obj_for_testing.fullTestDataframe()
        fdf = filter.filterDataframePerColumn(dft, "col1", 1000)
        assert len(fdf) == 0


class Test_filterDataframePerPeriod:
    """Tests for 'filterDataframePerPeriod' method."""

    obj_for_testing = ObjectsForTesting()

    lower_invalid_date = datetime.strptime("2020/10/01", "%Y/%m/%d")
    initial_date = datetime.strptime("2021/10/01", "%Y/%m/%d")
    medium_date = datetime.strptime("2021/10/04", "%Y/%m/%d")
    final_date = datetime.strptime("2021/10/06", "%Y/%m/%d")
    upper_invalid_date = datetime.strptime("2022/10/06", "%Y/%m/%d")

    # List of tuples, with the following order per tuple:
    # - dft, filter, ini_date, end_date
    validValues_list = [
        obj_for_testing.fullTestDataframe() + (initial_date, final_date),
        obj_for_testing.nonCol1TestDataframe() + (initial_date, final_date),
        obj_for_testing.nonCol2TestDataframe() + (initial_date, final_date),
        obj_for_testing.nonDateTestDataframe() + (initial_date, final_date),
        obj_for_testing.emptyTestDataframe() + (initial_date, final_date),
    ]

    # List of tuples, with the following order per tuple:
    # - ini_date, end_date, expected_len
    foundOK_dateList = [
        (initial_date, final_date, 6),
        (initial_date, medium_date, 4),
        (medium_date, final_date, 3),
        (lower_invalid_date, upper_invalid_date, 6),
        (upper_invalid_date, lower_invalid_date, 0),
    ]

    @pytest.mark.parametrize(
        "dft, filter, ini_date, end_date",
        validValues_list,
    )
    def test_validValues(self, dft, filter, ini_date, end_date):
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

    def test_nonValidValues(self):
        """Test the 'filterDataframePerPeriod' method against non-dataframes.

        An exception will be raised if non-dataframe type is used.
        """
        obj_for_testing = ObjectsForTesting()
        non_dft, filter = obj_for_testing.nonDataframe()
        ini_date = self.initial_date
        end_date = self.final_date
        with pytest.raises(TypeError):
            fdf = filter.filterDataframePerPeriod(
                non_dft,
                "date",
                ini_date,
                end_date,
            )

    @pytest.mark.parametrize(
        "ini_date, end_date, expected_len",
        foundOK_dateList,
    )
    def test_foundOK(self, ini_date, end_date, expected_len):
        """Check if the filter works correctly with some valid interval."""
        obj_for_testing = ObjectsForTesting()
        dft, filter = obj_for_testing.fullTestDataframe()
        fdf = filter.filterDataframePerPeriod(dft, "date", ini_date, end_date)
        assert len(fdf) == expected_len


class Test_getListFromDataframeColumn:
    """Tests for 'getListFromDataframeColumn' method."""

    obj_for_testing = ObjectsForTesting()

    # List of tuples, with the following order per tuple:
    # - dft, filter
    validValues_list = [
        obj_for_testing.fullTestDataframe(),
        obj_for_testing.nonCol1TestDataframe(),
        obj_for_testing.nonCol2TestDataframe(),
        obj_for_testing.nonDateTestDataframe(),
        obj_for_testing.emptyTestDataframe(),
    ]

    @pytest.mark.parametrize("dft, filter", validValues_list)
    def test_validValues(self, dft, filter):
        """Test the 'getListFromDataframeColumn' method against dataframes.

        The application will not brake if some column is not found.
        """
        result_list = filter.getListFromDataframeColumn(dft, "col1")
        assert isinstance(result_list, list) is True

    def test_nonValidValues(self):
        """Test the 'getListFromDataframeColumn' method against non-dataframes.

        An exception will be raised if non-dataframe type is used.
        """
        obj_for_testing = ObjectsForTesting()
        non_dft, filter = obj_for_testing.nonDataframe()
        with pytest.raises(TypeError):
            fdf = filter.getListFromDataframeColumn(non_dft, "col1")

    def test_foundOK(self):
        """Check if the filter works correctly with some valid values."""
        obj_for_testing = ObjectsForTesting()
        dft, filter = obj_for_testing.fullTestDataframe()
        fdf = filter.getListFromDataframeColumn(dft, "col1")
        assert len(fdf) == 6
