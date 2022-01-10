"""This file has a set of methods related to Fixed Income value estimation."""

import calendar
from datetime import datetime

from indexer_lib.interest_calculation import InterestCalculation


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

    def __getYearMonthDay(self, date):
        month = date.month
        year = date.year
        day = date.day
        return year, month, day

    def __getNumberOfMonths(self, year, month):
        # month => "1 to 12" needs to be "0 to 11"
        return (year * 12) + (month - 1)

    def __getMonthsPeriod(self, init_year, init_month, end_year, end_month):
        init = self.__getNumberOfMonths(init_year, init_month)
        end = self.__getNumberOfMonths(end_year, end_month)
        return (end - init) + 1

    def __getDaysPeriod(self, initial_date, final_date):
        return (final_date - initial_date).days + 1

    def __getDate(self, year, month, day):
        string_list = [str(year), str(month), str(day)]
        date_str = "-".join(string_list)
        return datetime.strptime(date_str, "%Y-%m-%d")

    def __getTotalDaysInMonth(self, year, month):
        range_tuple = calendar.monthrange(year, month)
        return range_tuple[1]

    def getValueByPrefixedRate(
        self,
        initial_date,
        final_date,
        rate,
        buy_price,
    ):
        """Return the final value given a prefixed interest rate."""
        # Calculate the total period in months and days
        init_y, init_m, init_d = self.__getYearMonthDay(initial_date)
        end_y, end_m, end_d = self.__getYearMonthDay(final_date)
        months_period = self.__getMonthsPeriod(init_y, init_m, end_y, end_m)
        days_period = self.__getDaysPeriod(initial_date, final_date)

        # Find the first day of the prefixed series
        pre_1st_day = self.__getDate(init_y, init_m, 1)

        # Find the last day of the prefixed series
        pre_last_day = self.__getTotalDaysInMonth(end_y, end_m)
        pre_end_date = self.__getDate(end_y, end_m, pre_last_day)

        # Calculate the proportion of days
        pre_days_period = self.__getDaysPeriod(pre_1st_day, pre_end_date)
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
        return buy_price + (int_value * day_proportion)
