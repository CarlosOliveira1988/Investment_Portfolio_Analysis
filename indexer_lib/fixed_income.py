"""This file has a set of methods related to Fixed Income value estimation."""

import calendar
from datetime import datetime

from indexer_lib.interest_calculation import Benchmark, InterestCalculation


class IndexerCalc(Benchmark):
    """Class used to get values related to CDI and IPCA."""

    def __init__(self):
        """Create the IndexerCalc object."""
        super().__init__()

    """Private methods."""

    def __setParameters(self, initial_date, final_date, buy_price):
        # Find the first day of first/last months of the series
        init_y, init_m, init_d = self._getYearMonthDay(initial_date)
        end_y, end_m, end_d = self._getYearMonthDay(final_date)

        # Get the indexer interest value
        # The monthly values are reported as 1st day of the month
        # But it takes in account the entire month
        day1_1st_month = self._getDate(init_y, init_m, 1)
        day1_last_month = self._getDate(end_y, end_m, 1)
        months_period = self._getMonthsPeriod(init_y, init_m, end_y, end_m)
        self.setValues(buy_price, buy_price)
        self.setPeriods(day1_1st_month, day1_last_month)
        self.setTotalMonths(months_period)

    """Protected methods."""

    def _getYearMonthDay(self, date):
        month = date.month
        year = date.year
        day = date.day
        return year, month, day

    def _getDate(self, year, month, day):
        string_list = [str(year), str(month), str(day)]
        date_str = "-".join(string_list)
        return datetime.strptime(date_str, "%Y-%m-%d")

    def _getMonthsPeriod(self, init_year, init_month, end_year, end_month):
        init = self._getNumberOfMonths(init_year, init_month)
        end = self._getNumberOfMonths(end_year, end_month)
        return (end - init) + 1

    def _getNumberOfMonths(self, year, month):
        return (year * 12) + (month - 1)

    def _getDaysPeriod(self, initial_date, final_date):
        return (final_date - initial_date).days + 1

    def _getTotalDaysInMonth(self, year, month):
        range_tuple = calendar.monthrange(year, month)
        return range_tuple[1]

    """Public methods."""

    def getInterestValueFromIPCA(self, initial_date, final_date, buy_price):
        """Return the interest value from IPCA."""
        self.__setParameters(initial_date, final_date, buy_price)
        return self._getInterestValueFromIndexer(self.getIPCA(), True)

    def getInterestValueFromCDI(self, initial_date, final_date, buy_price):
        """Return the interest value from CDI."""
        self.__setParameters(initial_date, final_date, buy_price)
        return self._getInterestValueFromIndexer(self.getCDI(), True)


class FixedIncomeCalculation:
    """This is a class to estimate Fixed Income current value.

    Usually, the real investments runs on weekdays. But, this class
    takes in account the total amount of days in a month (31 instead
    of 21)

    Then, for short periods (less than 1 month) we can see a huge error
    in the results when comparing to long periods (more than 3 months).
    """

    def __init__(self):
        """Create the FixedIncomeCalculation object."""
        self.interest = InterestCalculation()
        self.idx = IndexerCalc()

    """Protected methods."""

    def _getValueByPrefixedRate(
        self,
        initial_date,
        final_date,
        rate,
        buy_price,
    ):
        """Return the final value given a prefixed interest rate."""
        # Calculate the total period in months and days
        init_y, init_m, init_d = self.idx._getYearMonthDay(initial_date)
        end_y, end_m, end_d = self.idx._getYearMonthDay(final_date)
        months_period = self.idx._getMonthsPeriod(init_y, init_m, end_y, end_m)
        days_period = self.idx._getDaysPeriod(initial_date, final_date)

        # Find the first day of the prefixed series
        pre_1st_day = self.idx._getDate(init_y, init_m, 1)

        # Find the last day of the prefixed series
        pre_last_day = self.idx._getTotalDaysInMonth(end_y, end_m)
        pre_end_date = self.idx._getDate(end_y, end_m, pre_last_day)

        # Calculate the proportion of days
        pre_days_period = self.idx._getDaysPeriod(pre_1st_day, pre_end_date)
        day_proportion = days_period / pre_days_period

        # Calculate the final value
        mean_rate = self.interest.calculateMeanInterestRatePerPeriod(
            rate,
            12,
        )
        rate_list = self.interest.getPrefixedInterestRateList(
            mean_rate,
            months_period,
        )
        int_value = self.interest.calculateInterestValue(rate_list, buy_price)
        final_value = buy_price + (int_value * day_proportion)
        return final_value, day_proportion

    """Public methods."""

    def getValueByPrefixedRate(
        self,
        initial_date,
        final_date,
        rate,
        buy_price,
    ):
        """Return the final value given a prefixed interest rate."""
        prefixed_tuple = self._getValueByPrefixedRate(
            initial_date,
            final_date,
            rate,
            buy_price,
        )
        return prefixed_tuple[0]

    def getValueByPrefixedRatePlusIPCA(
        self,
        initial_date,
        final_date,
        rate,
        buy_price,
    ):
        """Return the final value given a prefixed interest rate + IPCA."""
        # Calculate the amount of interest value related to the prefixed rate
        prefixed_value, day_proportion = self._getValueByPrefixedRate(
            initial_date,
            final_date,
            rate,
            buy_price,
        )
        prefixed_interest = prefixed_value - buy_price

        # Calculate the amount of interest value related to the IPCA
        IPCA_interest_value = self.idx.getInterestValueFromIPCA(
            initial_date,
            final_date,
            buy_price,
        )
        IPCA_interest = IPCA_interest_value * day_proportion

        # Return the total amount of value
        return buy_price + prefixed_interest + IPCA_interest

    def getValueByProportionalCDI(
        self,
        initial_date,
        final_date,
        rate,
        buy_price,
    ):
        """Return the final value given a proportional CDI interest rate."""
        # Calculate the day proportion
        trash, day_proportion = self._getValueByPrefixedRate(
            initial_date,
            final_date,
            rate,
            buy_price,
        )

        # Calculate the amount of interest value related to the CDI
        CDI_interest_value = self.idx.getInterestValueFromCDI(
            initial_date,
            final_date,
            buy_price,
        )
        CDI_interest = CDI_interest_value * rate * day_proportion

        # Return the total amount of value
        return buy_price + CDI_interest
