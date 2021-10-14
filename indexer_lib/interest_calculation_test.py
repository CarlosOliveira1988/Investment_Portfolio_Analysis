"""This file is used to test the 'interest_calculation.py'."""

import pytest

from indexer_lib.interest_calculation import InterestCalculation


class Test_InterestCalculation:
    """Tests for 'InterestCalculation' class."""

    # List of tuples, with the following order per tuple:
    # - initial_value, final_value, expected_value
    test_calculateInterestValueByValues_list = [
        (1500.0, 2000.0, 500.0),
        (1500.0, 1000.0, -500.0),
        (0.0, 500.0, 500.0),
        (500.0, 0.0, -500.0),
        (-500.0, 0.0, 500.0),
        (-500.0, -1000.0, -500.0),
    ]

    # List of tuples, with the following order per tuple:
    # - interest_rate_list, initial_value, expected_value
    test_calculateInterestValue_list = [
        ([0.01], 1000.0, 10.0),
        ([0.01] * 12, 1000.0, 126.82),
        ([0.01, 0.01, 0.01, -0.01], 1000.0, 19.99),
        ([-0.01, 0.01, 0.01, 0.01], 1000.0, 19.99),
    ]

    # List of tuples, with the following order per tuple:
    # - interest_rate_list, initial_value, expected_value_list
    test_getCumulativeInterestValueList_list = [
        ([0.01], 1000.0, [10.0]),
        ([0.01, 0.01], 1000.0, [10.0, 10.1]),
        ([0.01, 0.01, 0.01], 1000.0, [10.0, 10.1, 10.201]),
        ([0.01, 0.01, -0.01], 1000.0, [10.0, 10.1, -10.201]),
        ([0.01, 0.01, 0.01], 0.0, [0.0, 0.0, 0.0]),
    ]

    def getInterestCalculationObject(self):
        """Return the InterestCalculation object under testing."""
        return InterestCalculation()

    @pytest.mark.parametrize(
        "initial_value, final_value, expected_value",
        test_calculateInterestValueByValues_list,
    )
    def test_calculateInterestValueByValues(
        self, initial_value, final_value, expected_value
    ):
        """Test the 'calculateInterestValueByValues' method."""
        interest_calculation = self.getInterestCalculationObject()
        assert (
            interest_calculation.calculateInterestValueByValues(
                initial_value, final_value
            )
            == expected_value
        )

    def test_calculateInterestValueByValues_exceptions(self):
        """Test the 'calculateInterestValueByValues' method with exceptions."""
        interest_calculation = self.getInterestCalculationObject()
        with pytest.raises(TypeError):
            interest_calculation.calculateInterestValueByValues("True", 0)
        with pytest.raises(TypeError):
            interest_calculation.calculateInterestValueByValues(0, "True")

    @pytest.mark.parametrize(
        "interest_rate_list, initial_value, expected_value",
        test_calculateInterestValue_list,
    )
    def test_calculateInterestValue(
        self, interest_rate_list, initial_value, expected_value
    ):
        """Test the 'calculateInterestValue' method."""
        interest_calculation = self.getInterestCalculationObject()
        assert interest_calculation.calculateInterestValue(
            interest_rate_list, initial_value
        ) == pytest.approx(expected_value, 0.01)

    def test_calculateInterestValue_exceptions(self):
        """Test the 'calculateInterestValue' method with exceptions."""
        interest_calculation = self.getInterestCalculationObject()
        with pytest.raises(ValueError):
            interest_calculation.calculateInterestValue([], 1000.0)
        with pytest.raises(TypeError):
            interest_calculation.calculateInterestValue(["True"], 1000.0)
        with pytest.raises(TypeError):
            interest_calculation.calculateInterestValue([0.01, "True"], 1000.0)
        with pytest.raises(TypeError):
            interest_calculation.calculateInterestValue(["True", 0.01], 1000.0)
        with pytest.raises(TypeError):
            interest_calculation.calculateInterestValue([0.01, 0.01], "True")

    @pytest.mark.parametrize(
        "interest_rate_list, initial_value, expected_value_list",
        test_getCumulativeInterestValueList_list,
    )
    def test_getCumulativeInterestValueList(
        self, interest_rate_list, initial_value, expected_value_list
    ):
        """Test the 'getCumulativeInterestValueList' method."""
        interest_calculation = self.getInterestCalculationObject()
        value_list = interest_calculation.getCumulativeInterestValueList(
            interest_rate_list, initial_value
        )
        for i in range(len(value_list)):
            assert value_list[i] == pytest.approx(expected_value_list[i], 0.01)

    def test_getCumulativeInterestValueList_exceptions(self):
        """Test the 'getCumulativeInterestValueList' method with exceptions."""
        interest_calculation = self.getInterestCalculationObject()
        with pytest.raises(ValueError):
            interest_calculation.getCumulativeInterestValueList(
                [],
                1000.0,
            )
        with pytest.raises(TypeError):
            interest_calculation.getCumulativeInterestValueList(
                ["True"],
                1000.0,
            )
        with pytest.raises(TypeError):
            interest_calculation.getCumulativeInterestValueList(
                [0.01, "True"],
                1000.0,
            )
        with pytest.raises(TypeError):
            interest_calculation.getCumulativeInterestValueList(
                ["True", 0.01],
                1000.0,
            )
        with pytest.raises(TypeError):
            interest_calculation.getCumulativeInterestValueList(
                [0.01, 0.01],
                "True",
            )

    def test_getCumulativeInterestRateList(self):
        """Test the 'getCumulativeInterestRateList' method."""
        interest_calculation = self.getInterestCalculationObject()
        rate_list = interest_calculation.getCumulativeInterestRateList(
            [100.0, 110.0, 121.0], 1000
        )
        assert rate_list == [0.1, 0.1, 0.1]  # 0.1 means 10.0%

    def test_calculateInterestRateByValues(self):
        """Test the 'calculateInterestRateByValues' method."""
        interest_calculation = self.getInterestCalculationObject()
        rate = interest_calculation.calculateInterestRateByValues(1000, 2000)
        assert rate == 1.0  # 1.0 means 100.0%

    def test_calculateInterestRate(self):
        """Test the 'calculateInterestRate' method."""
        interest_calculation = self.getInterestCalculationObject()
        rate = interest_calculation.calculateInterestRate(
            [0.1, 0.1, 0.1],
            1000,
        )
        assert rate == 0.331  # 0.331 means 33.1%

    def test_calculateMeanInterestRatePerPeriod(self):
        """Test the 'calculateMeanInterestRatePerPeriod' method."""
        interest_calculation = self.getInterestCalculationObject()
        rate_value = interest_calculation.calculateMeanInterestRatePerPeriod(
            0.0616778118644995687897076174316, 12
        )
        assert rate_value == pytest.approx(0.005, 0.001)  # 0.005 means 0.5%

    def test_getPrefixedInterestRateList(self):
        """Test the 'getPrefixedInterestRateList' method."""
        interest_calculation = self.getInterestCalculationObject()
        rate_list = interest_calculation.getPrefixedInterestRateList(0.01, 5)
        assert rate_list == [0.01, 0.01, 0.01, 0.01, 0.01]  # 0.01 means 1.0%
