import math


class InterestCalculation:
    """
    This class is useful to calculate 'Interest Value' and 'Interest Rate'.

    The 'Interest Value' (a float number) is the total amount of value, usually expressed in 'R$'.
    Example: 1000.0 (R$)

    The 'Interest Rate' (a float number) is the portion/fraction of interest, usually expressed in '%'.
    Example: 6.02 (%)

    The 'Interest Rate' in this class may be expressed in 2 different ways as shown in the example.
    Example: 6.02 (%) => 6.02 or 0.0602

    By the default, the '0.0602' format (divide_rates_by_100=False) is adopted. It means, you need
    to work with 'raw' rates. If you prefer to work with 'adjusted' rates like '6.02', then set
    the flag correctly (divide_rates_by_100=True).
    """
    def __init__(self, divide_rates_by_100=False):
        self.__divide_rates_by_100 = divide_rates_by_100

    def setDividedRatesBy100(self, divide_rates_by_100):
        """
        Sets the value of the 'divide_rates_by_100' flag.
        - False: the value '6.02 (%)' is represented by the float '0.0602'
        - True:  the value '6.02 (%)' is represented by the float '6.02'
        """
        self.__divide_rates_by_100 = divide_rates_by_100

    def getDividedRatesBy100(self):
        """
        Returns the value of the 'divide_rates_by_100' flag.
        """
        return self.__divide_rates_by_100

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
        
        Note related to the 'divide_rates_by_100' flag: if TRUE: 0.62% -> 0.0062 / if FALSE: 0.62% -> 0.62
        """
        total_value = initial_value
        for interest_rate in interest_rate_list:
            interest_rate = float(interest_rate)
            if math.isnan(interest_rate):
                interest_rate = 0.0
            if self.__divide_rates_by_100:
                adjusted_interest_rate = (1 + interest_rate/100.0)
            else:
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

        Note related to the 'divide_rates_by_100' flag: if TRUE: 0.62 -> 62.00% / if FALSE: 0.62 -> 0.62%
        """
        total_interest_rate = self.calculateInterestValueByValues(initial_value, final_value) / initial_value
        if self.__divide_rates_by_100:
            total_interest_rate *= 100.0
        return total_interest_rate

    def calculateInterestRate(self, interest_rate_list, initial_value=1.00):
        """
        Calculates the total interest rate based on an 'interest rate list' and an 'initial value'.

        Arguments:
        - interest_rate_list(float): a list of interest rates
        - initial_value(float): the initial value

        Note related to the 'divide_rates_by_100' flag: if TRUE: 0.62% -> 0.0062 / if FALSE: 0.62% -> 0.62
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
    Private methods
    """
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

    def setFinalValue(self, value):
        self.final_value = value

    def getFinalValue(self):
        return self.final_value

    def setInterestValue(self, value):
        self.interest_value = value

    def getInterestValue(self):
        return self.interest_value

    def setInterestRate(self, value):
        self.interest_rate = value

    def getInterestRate(self):
        return self.interest_rate

    def setInterestRateList(self, value_list):
        self.interest_rate_list = value_list

    def getInterestRateList(self):
        return self.interest_rate_list

    def setInterestValueList(self, value_list):
        self.interest_value_list = value_list

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
        self.setFinalValue(final_value)
        self.setInterestValue(self.InterestCalculation.calculateInterestValueByValues(self.getInitialValue(), self.getFinalValue()))
        self.setInterestValueList(cumulative_interest_value_list)
        self.setInterestRate(self.InterestCalculation.calculateInterestRateByValues(self.getInitialValue(), self.getFinalValue()))
        self.setInterestRateList(cumulative_monthly_interest_rate_list)


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

    def calculateValues(self):
        self._calculate(self.input_interest_rate_list)
        cumulative_interest_value_list = [value*self.interest_rate_factor for value in self.getInterestValueList()]
        cumulative_monthly_interest_rate_list = self.InterestCalculation.getCumulativeInterestRateList(cumulative_interest_value_list, self.getInitialValue())
        final_value = self.getInitialValue() + self.InterestCalculation.calculateInterestValue(cumulative_monthly_interest_rate_list, self.getInitialValue())
        self.setFinalValue(final_value)
        self.setInterestValue(self.InterestCalculation.calculateInterestValueByValues(self.getInitialValue(), self.getFinalValue()))
        self.setInterestValueList(cumulative_interest_value_list)
        self.setInterestRate(self.InterestCalculation.calculateInterestRateByValues(self.getInitialValue(), self.getFinalValue()))
        self.setInterestRateList(cumulative_monthly_interest_rate_list)
