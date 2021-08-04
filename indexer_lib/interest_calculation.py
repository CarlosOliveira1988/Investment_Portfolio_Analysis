import math


class InterestCalculation:
    """
    This class is useful to calculate 'Interest Value' and 'Interest Rate'.

    The 'Interest Value' (a float number) is the total amount of value, usually expressed in 'R$'.
    Example: 1000.0 (R$)

    The 'Interest Rate' (a float number) is the portion/fraction of interest, usually expressed in '%'.
    Example: 6.02 (%)

    The 'Interest Rate' in this class is expressed in a 'raw' way, where '0.0602' means '6.02%'.
    """
    def __init__(self):
        pass

    def calculateInterestValueByValues(self, initial_value, final_value):
        """
        Calculates the total interest value based on 'initial' and 'final' values.
        Basically, returns the difference between the 'final' and 'initial' values.

        Arguments:
        - initial_value(float)
        - final_value(float)
        """
        return final_value - initial_value

    def calculateInterestValue(self, interest_rate_list, initial_value=1.00):
        """
        Calculates the total interest value based on an 'interest rate list' and an 'initial value'.

        'NaN' values are replaced by the '0.0' constant.

        Arguments:
        - interest_rate_list(float): a list of interest rates
        - initial_value(float): the initial value
        """
        total_value = initial_value
        for interest_rate in interest_rate_list:
            interest_rate = float(interest_rate)
            if math.isnan(interest_rate):
                interest_rate = 0.0
            adjusted_interest_rate = (1 + interest_rate)
            total_value = adjusted_interest_rate * total_value
        return self.calculateInterestValueByValues(initial_value, total_value)

    def getCumulativeInterestValueList(self, interest_rate_list, initial_value=1.00):
        """
        Given an 'interest_rate_list' and an 'initial_value', returns an 'interest_values_list'
        with the same length.

        Example: 
        - interest_rate_list = [0.01, 0.02, 0.03, 0.04, 0.05]
        - initial_value = 1000
        - output = [10.0, 20.0, 30.0, 40.0, 50.0]
        """
        cumulative_interest_value_list = []
        total_value = initial_value
        for interest_rate in interest_rate_list:
            cumulative_interest_value = self.calculateInterestValue([interest_rate], total_value)
            cumulative_interest_value_list.append(cumulative_interest_value)
            total_value += cumulative_interest_value
        return cumulative_interest_value_list

    def getCumulativeInterestRateList(self, interest_value_list, initial_value=1.00):
        """
        Given an 'interest_value_list' and an 'initial_value', returns an 'interest_rate_list'
        with the same length.

        Example: 
        - interest_value_list = [100.0, 110.0, 121.0]
        - initial_value = 1000
        - output = [0.1, 0.1, 0.1]
        """
        mean_interest_rate_list = []
        interest_value_per_period = initial_value
        for interest_value in interest_value_list:
            mean_interest_rate = self.calculateInterestRateByValues(interest_value_per_period, (interest_value_per_period+interest_value))
            mean_interest_rate_list.append(mean_interest_rate)
            interest_value_per_period = (interest_value_per_period+interest_value)
        return mean_interest_rate_list

    def calculateInterestRateByValues(self, initial_value, final_value):
        """
        Calculates the total interest rate based on 'initial' and 'final' values.

        Arguments:
        - initial_value(float)
        - final_value(float)
        """
        total_interest_rate = self.calculateInterestValueByValues(initial_value, final_value) / initial_value
        return total_interest_rate

    def calculateInterestRate(self, interest_rate_list, initial_value=1.00):
        """
        Calculates the total interest rate based on an 'interest rate list' and an 'initial value'.

        Arguments:
        - interest_rate_list(float): a list of interest rates
        - initial_value(float): the initial value
        """
        interest_value = self.calculateInterestValue(interest_rate_list, initial_value)
        total_interest_rate = self.calculateInterestRateByValues(initial_value, (initial_value+interest_value))
        return total_interest_rate

    def calculateMeanInterestRatePerPeriod(self, interest_rate, number_of_periods):
        """
        Given an 'interest_rate' and a 'number_of_periods', returns the 'mean_interest_rate' related
        to the period.

        Example:
        - interest_rate = 0.0616778118644995687897076174316
        - number_of_periods = 12
        - output = 0.005
        """
        mean_interest_rate_per_period = (1+interest_rate) ** (1/number_of_periods)
        mean_interest_rate_per_period -= 1
        return mean_interest_rate_per_period

    def getPrefixedInterestRateList(self, prefixed_interest_rate, number_of_periods):
        """
        Returns n 'interest_rate_list' given a 'prefixed_interest_rate' and a 'number_of_periods'.

        Example:
        - prefixed_interest_rate = 0.01
        - number_of_periods = 12
        - output = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        """
        return [prefixed_interest_rate] * number_of_periods


class InterestOnCurve:
    """
    This is a based class used to calculate values/lists related to 'interest_values' and 'interest_rates'.

    Basically, given an 'initial_value' and an 'interest_rate_list', we may calculate and provide to the user
    a set of values and curves, useful to show data and plots to the user.

    This class is also a kind of interface to other classes.
    """
    def __init__(self, initial_value, interest_rate_list):
        self.InterestCalculation = InterestCalculation()
        self.initial_value = initial_value
        self.interest_rate_list = interest_rate_list
        self.final_value = 0
        self.interest_value = 0
        self.interest_rate = 0
        self.interest_value_list = []
        self.final_interest_rate_list = []

    """
    Protected methods
    """
    def _setFinalValue(self, value):
        self.final_value = value

    def _setInterestValue(self, value):
        self.interest_value = value

    def _setInterestRate(self, value):
        self.interest_rate = value

    def _setInterestRateList(self, value_list):
        self.interest_rate_list = value_list

    def _setInterestValueList(self, value_list):
        self.interest_value_list = value_list

    def _calculate(self, external_interest_rate_list=None):
        if external_interest_rate_list:
            interest_rate_list = external_interest_rate_list
        else:
            interest_rate_list = self.interest_rate_list
        self.interest_value = self.InterestCalculation.calculateInterestValue(interest_rate_list, self.initial_value)
        self.final_value = self.initial_value + self.interest_value
        self.interest_rate = self.InterestCalculation.calculateInterestRateByValues(self.initial_value, self.final_value)
        self.interest_value_list = self.InterestCalculation.getCumulativeInterestValueList(interest_rate_list, self.initial_value)

    """
    Puclic methods
    """
    def getInitialValue(self):
        return self.initial_value

    def getFinalValue(self):
        return self.final_value

    def getInterestValue(self):
        return self.interest_value

    def getInterestRate(self):
        return self.interest_rate

    def getInterestRateList(self):
        return self.interest_rate_list

    def getInterestValueList(self):
        return self.interest_value_list

    def calculateValues(self):
        self._calculate()


class InterestOnCurvePrefixed(InterestOnCurve):
    """
    This is a based class used to calculate values/lists related to 'interest_values' and 'interest_rates'.

    Basically, given an 'initial_value', an 'interest_rate_list' and an 'yearly_additional_interest_rate', 
    we may calculate and provide to the user a set of values and curves, useful to show data and plots to 
    the user.
    """
    def __init__(self, initial_value, interest_rate_list, yearly_additional_interest_rate):
        super().__init__(initial_value, interest_rate_list)
        self.input_interest_rate_list = interest_rate_list
        self.additional_interest_rate = yearly_additional_interest_rate
        self.additional_interest_rate_period = 12
        self.additional_interest_rate_per_month = self.InterestCalculation.calculateMeanInterestRatePerPeriod(self.additional_interest_rate, self.additional_interest_rate_period)

    """
    Puclic methods
    """
    def getYearlyPrefixedInterestRate(self):
        return self.additional_interest_rate

    def getMonthlyPrefixedInterestRate(self):
        return self.additional_interest_rate_per_month

    def calculateValues(self):
        self._calculate(self.input_interest_rate_list)
        additional_monthly_interest_rate_list = self.InterestCalculation.getPrefixedInterestRateList(self.additional_interest_rate_per_month, len(self.input_interest_rate_list))
        additional_cumulative_interest_value_list = self.InterestCalculation.getCumulativeInterestValueList(additional_monthly_interest_rate_list, self.getInitialValue())
        cumulative_interest_value_list = [sum(values) for values in zip(self.getInterestValueList(), additional_cumulative_interest_value_list)]
        cumulative_monthly_interest_rate_list = self.InterestCalculation.getCumulativeInterestRateList(cumulative_interest_value_list, self.getInitialValue())
        final_value = self.getInitialValue() + self.InterestCalculation.calculateInterestValue(cumulative_monthly_interest_rate_list, self.getInitialValue())
        self._setFinalValue(final_value)
        self._setInterestValue(self.InterestCalculation.calculateInterestValueByValues(self.getInitialValue(), self.getFinalValue()))
        self._setInterestValueList(cumulative_interest_value_list)
        self._setInterestRate(self.InterestCalculation.calculateInterestRateByValues(self.getInitialValue(), self.getFinalValue()))
        self._setInterestRateList(cumulative_monthly_interest_rate_list)


class InterestOnCurveProportional(InterestOnCurve):
    """
    This is a based class used to calculate values/lists related to 'interest_values' and 'interest_rates'.

    Basically, given an 'initial_value', an 'interest_rate_list' and an 'interest_rate_factor', we may calculate 
    and provide to the user a set of values and curves, useful to show data and plots to the user.
    """
    def __init__(self, initial_value, interest_rate_list, interest_rate_factor):
        super().__init__(initial_value, interest_rate_list)
        self.input_interest_rate_list = interest_rate_list
        self.interest_rate_factor = interest_rate_factor

    """
    Puclic methods
    """
    def calculateValues(self):
        self._calculate(self.input_interest_rate_list)
        cumulative_interest_value_list = [value*self.interest_rate_factor for value in self.getInterestValueList()]
        cumulative_monthly_interest_rate_list = self.InterestCalculation.getCumulativeInterestRateList(cumulative_interest_value_list, self.getInitialValue())
        final_value = self.getInitialValue() + self.InterestCalculation.calculateInterestValue(cumulative_monthly_interest_rate_list, self.getInitialValue())
        self._setFinalValue(final_value)
        self._setInterestValue(self.InterestCalculation.calculateInterestValueByValues(self.getInitialValue(), self.getFinalValue()))
        self._setInterestValueList(cumulative_interest_value_list)
        self._setInterestRate(self.InterestCalculation.calculateInterestRateByValues(self.getInitialValue(), self.getFinalValue()))
        self._setInterestRateList(cumulative_monthly_interest_rate_list)


class Benchmark:
    """
    This class is useful to perform comparison with common Benchmarks used in the market, such as
    IPCA and SELIC.

    Also, we can get the interest rates in a 'monthly basis' and in an 'yearly basis'.
    """
    def __init__(self):
        from indexer_manager import StackedFormatConstants
        from dataframe_filter import DataframeFilter
        from economic_indexers import CDI
        from economic_indexers import IPCA
        self.InterestCalculation = InterestCalculation()
        self.StackedFormatConstants = StackedFormatConstants()
        self.DataframeFilter = DataframeFilter()
        self.CDI = CDI()
        self.IPCA = IPCA()
        self.initial_value = 0
        self.final_value = 0
        self.interest_value = 0
        self.initial_period = None
        self.final_period = None
        self.total_months = 0

    """
    Private methods
    """
    def __getInterestValueFromIndexer(self, economic_indexer):
        dataframe = economic_indexer.getDataframe()
        filtered_dataframe = self.DataframeFilter.filterDataframePerPeriod(dataframe, self.StackedFormatConstants.getAdjustedDateTitle(), self.initial_period, self.final_period)
        monthly_interest_rate_list = self.DataframeFilter.getListFromDataframeColumn(filtered_dataframe, self.StackedFormatConstants.getInterestTitle())
        return self.InterestCalculation.calculateInterestValue(monthly_interest_rate_list, self.initial_value)

    """
    Public methods
    """
    def setValues(self, initial_value, final_value):
        self.initial_value = initial_value
        self.final_value = final_value
    
    def setPeriods(self, initial_period, final_period):
        self.initial_period = initial_period
        self.final_period = final_period
    
    def setTotalMonths(self, total_months):
        self.total_months = total_months

    def getMonthlyEquivalentInterestRate(self):
        interest_rate = self.InterestCalculation.calculateInterestRateByValues(self.initial_value, self.final_value)
        return self.InterestCalculation.calculateMeanInterestRatePerPeriod(interest_rate, self.total_months)

    def getYearlyEquivalentInterestRate(self):
        equivalent_monthly = self.getMonthlyEquivalentInterestRate()
        equivalent_monthly_list = self.InterestCalculation.getPrefixedInterestRateList(equivalent_monthly, 12)
        return self.InterestCalculation.calculateInterestRate(equivalent_monthly_list)

    def getCDIEquivalentInterestRate(self):
        interest_value = self.InterestCalculation.calculateInterestValueByValues(self.initial_value, self.final_value)
        cdi_interest_value = self.__getInterestValueFromIndexer(self.CDI)
        return interest_value / cdi_interest_value

    def getIPCAEquivalentInterestRate(self):
        interest_value = self.InterestCalculation.calculateInterestValueByValues(self.initial_value, self.final_value)
        ipca_interest_value = self.__getInterestValueFromIndexer(self.IPCA)
        prefixed_interest_value = interest_value - ipca_interest_value
        prefixed_interest_rate = self.InterestCalculation.calculateInterestRateByValues(self.initial_value, (self.initial_value+prefixed_interest_value))
        monthly_prefixed_interest_rate = self.InterestCalculation.calculateMeanInterestRatePerPeriod(prefixed_interest_rate, self.total_months)
        monthly_prefixed_interest_rate_list = self.InterestCalculation.getPrefixedInterestRateList(monthly_prefixed_interest_rate, 12)
        return self.InterestCalculation.calculateInterestRate(monthly_prefixed_interest_rate_list)
