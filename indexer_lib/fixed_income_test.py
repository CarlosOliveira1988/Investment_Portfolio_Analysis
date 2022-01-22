"""This file is used to test the 'fixed_income.py'."""

from datetime import datetime

import pytest

from indexer_lib.fixed_income import FixedIncomeCalculation, IndexerCalc


def date(string):
    """Return a date from the string."""
    return datetime.strptime(string, "%Y/%m/%d")


def dateToday():
    """Return a date from the string."""
    return datetime.today()


class Test_IndexerCalc:
    """Tests for 'IndexerCalc' class."""

    # List of tuples, with the following order per tuple:
    # - initial_date, final_date, buy_price, interest
    test_getInterestValueFromIPCA_list = [
        (date("2000/01/01"), date("2000/12/01"), 1000.0, 59.743),
        (date("2000/01/01"), date("2000/12/31"), 1000.0, 59.743),
        (date("2000/01/01"), date("2000/12/01"), 0.0, 0.0),
    ]

    # List of tuples, with the following order per tuple:
    # - initial_date, final_date, buy_price, interest
    test_getInterestValueFromCDI_list = [
        (date("2000/01/01"), date("2000/12/01"), 1000.0, 173.189),
        (date("2000/01/01"), date("2000/12/31"), 1000.0, 173.189),
        (date("2000/01/01"), date("2000/12/01"), 0.0, 0.0),
    ]

    @pytest.mark.parametrize(
        "initial_date, final_date, buy_price, interest",
        test_getInterestValueFromIPCA_list,
    )
    def test_getInterestValueFromIPCA(
        self, initial_date, final_date, buy_price, interest
    ):
        """Test the 'getInterestValueFromIPCA' method."""
        idxCalc = IndexerCalc()
        value = idxCalc.getInterestValueFromIPCA(
            initial_date,
            final_date,
            buy_price,
        )
        assert value == pytest.approx(interest, 0.001)

    def test_getInterestValueFromIPCA_today(self):
        """Test the 'getInterestValueFromIPCA' method."""
        idxCalc = IndexerCalc()
        value = idxCalc.getInterestValueFromIPCA(
            date("2000/01/01"),
            dateToday(),
            1000.0,
        )
        # Uncertain value but:
        # From 2000/01/01 to 2021/12/31:
        # 21 years = R$ 2.824,69
        assert value > 2820.0

    @pytest.mark.parametrize(
        "initial_date, final_date, buy_price, interest",
        test_getInterestValueFromCDI_list,
    )
    def test_getInterestValueFromCDI(
        self, initial_date, final_date, buy_price, interest
    ):
        """Test the 'getInterestValueFromCDI' method."""
        idxCalc = IndexerCalc()
        value = idxCalc.getInterestValueFromCDI(
            initial_date,
            final_date,
            buy_price,
        )
        assert value == pytest.approx(interest, 0.001)

    def test_getInterestValueFromCDI_today(self):
        """Test the 'getInterestValueFromCDI' method."""
        idxCalc = IndexerCalc()
        value = idxCalc.getInterestValueFromCDI(
            date("2000/01/01"),
            dateToday(),
            1000.0,
        )
        # Uncertain value but:
        # From 2000/01/01 to 2021/12/31:
        # 21 years = R$ 11.011,04
        assert value > 11011.0


class Test_FixedIncomeCalculation:
    """Tests for 'FixedIncomeCalculation' class."""

    # List of tuples, with the following order per tuple:
    # - initial_date, final_date, rate, buy_price, interest
    test_getValueByPrefixedRate_list = [
        (date("2000/01/01"), date("2000/12/31"), 0.12, 1000.0, 1120.0),
        (date("2000/01/01"), date("2000/12/31"), 0.0, 1000.0, 1000.0),
        (date("2000/01/01"), date("2000/12/31"), 0.12, 0.0, 0.0),
        (date("2000/04/01"), date("2000/04/15"), 0.12, 1000.0, 1004.744),
        (date("2000/04/01"), date("2000/04/30"), 0.12, 1000.0, 1009.489),
    ]

    # List of tuples, with the following order per tuple:
    # - initial_date, final_date, rate, buy_price, interest
    test_getValueByPrefixedRatePlusIPCA_list = [
        (date("2000/01/01"), date("2000/12/31"), 0.12, 1000.0, 1179.743),
        (date("2000/01/01"), date("2000/12/31"), 0.0, 1000.0, 1059.743),
        (date("2000/01/01"), date("2000/12/31"), 0.12, 0.0, 0.0),
        (date("2000/04/01"), date("2000/04/15"), 0.12, 1000.0, 1006.845),
        (date("2000/04/01"), date("2000/04/30"), 0.12, 1000.0, 1013.690),
    ]

    # List of tuples, with the following order per tuple:
    # - initial_date, final_date, rate, buy_price, interest
    test_getValueByProportionalCDI_list = [
        (date("2000/01/01"), date("2000/12/31"), 1.30, 1000.0, 1225.150),
        (date("2000/01/01"), date("2000/12/31"), 0.0, 1000.0, 1000.0),
        (date("2000/01/01"), date("2000/12/31"), 1.30, 0.0, 0.0),
        (date("2000/04/01"), date("2000/04/15"), 1.30, 1000.0, 1008.320),
        (date("2000/04/01"), date("2000/04/30"), 1.30, 1000.0, 1016.640),
    ]

    @pytest.mark.parametrize(
        "initial_date, final_date, rate, buy_price, interest",
        test_getValueByPrefixedRate_list,
    )
    def test_getValueByPrefixedRate(
        self, initial_date, final_date, rate, buy_price, interest
    ):
        """Test the 'getValueByPrefixedRate' method."""
        idxCalc = FixedIncomeCalculation()
        value = idxCalc.getValueByPrefixedRate(
            initial_date,
            final_date,
            rate,
            buy_price,
        )
        assert value == pytest.approx(interest, 0.001)

    def test_getValueByPrefixedRate_today(self):
        """Test the 'getValueByPrefixedRate' method."""
        idxCalc = FixedIncomeCalculation()
        value = idxCalc.getValueByPrefixedRate(
            date("2000/01/01"),
            dateToday(),
            0.01,
            1000.0,
        )
        # Uncertain value but:
        # From 2000/01/01 to 2021/12/31 at 1%/year:
        # 21 years = R$ 1.232,39
        assert value > 1232.0

    @pytest.mark.parametrize(
        "initial_date, final_date, rate, buy_price, interest",
        test_getValueByPrefixedRatePlusIPCA_list,
    )
    def test_getValueByPrefixedRatePlusIPCA(
        self, initial_date, final_date, rate, buy_price, interest
    ):
        """Test the 'getValueByPrefixedRatePlusIPCA' method."""
        idxCalc = FixedIncomeCalculation()
        value = idxCalc.getValueByPrefixedRatePlusIPCA(
            initial_date,
            final_date,
            rate,
            buy_price,
        )
        assert value == pytest.approx(interest, 0.001)

    def test_getValueByPrefixedRatePlusIPCA_today(self):
        """Test the 'getValueByPrefixedRatePlusIPCA' method."""
        idxCalc = FixedIncomeCalculation()
        value = idxCalc.getValueByPrefixedRatePlusIPCA(
            date("2000/01/01"),
            dateToday(),
            0.01,
            1000.0,
        )
        # Uncertain value but:
        # From 2000/01/01 to 2021/11/30 at 1%/year:
        # 21 years = R$ 4.068,38
        assert value > 4068.0

    @pytest.mark.parametrize(
        "initial_date, final_date, rate, buy_price, interest",
        test_getValueByProportionalCDI_list,
    )
    def test_getValueByProportionalCDI(
        self, initial_date, final_date, rate, buy_price, interest
    ):
        """Test the 'getValueByProportionalCDI' method."""
        idxCalc = FixedIncomeCalculation()
        value = idxCalc.getValueByProportionalCDI(
            initial_date,
            final_date,
            rate,
            buy_price,
        )
        assert value == pytest.approx(interest, 0.001)

    def test_getValueByProportionalCDI_today(self):
        """Test the 'getValueByProportionalCDI' method."""
        idxCalc = FixedIncomeCalculation()
        value = idxCalc.getValueByProportionalCDI(
            date("2000/01/01"),
            dateToday(),
            1.30,
            1000.0,
        )
        # Uncertain value but:
        # From 2000/01/01 to 2021/11/30 at 130%:
        # 21 years = R$ 15.314,35
        assert value > 15314.0
