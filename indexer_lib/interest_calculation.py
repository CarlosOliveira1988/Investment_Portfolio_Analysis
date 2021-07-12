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

        Arguments:
        - interest_rate_list(float): a list of interest rates
        - initial_value(float): the initial value
        
        Note related to the 'divide_rates_by_100' flag: if TRUE: 0.62% -> 0.0062 / if FALSE: 0.62% -> 0.62
        """
        total_interest_value = initial_value
        for interest_rate in interest_rate_list:
            if self.__divide_rates_by_100:
                adjusted_interest_rate = (1 + interest_rate/100.0)
            else:
                adjusted_interest_rate = (1 + interest_rate)
            total_interest_value = adjusted_interest_rate * total_interest_value
        return total_interest_value

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
        final_value = self.calculateInterestValue(interest_rate_list, initial_value)
        total_interest_rate = self.calculateInterestRateByValues(initial_value, final_value)
        return total_interest_rate
