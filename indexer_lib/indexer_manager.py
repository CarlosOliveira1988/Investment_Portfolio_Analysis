import calendar
from datetime import *
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import *

from indexer_lib.indexer_formater import OriginalIndexerFormater, StackedIndexerFormater
from indexer_lib.interest_calculation import InterestCalculation


class OriginalFormatConstants:

    # Constants related to the months
    MONTHS_LIST = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    # Contants related to the "Original" dataframe format (14 columns: similar to the observed in the Excel file)
    ORIGINAL_YEAR_COLUMN = "Ano"
    ORIGINAL_YEARLY_RATE_COLUMN = "Anual"
    ORIGINAL_FORMAT_COLUMNS = [ORIGINAL_YEAR_COLUMN]
    ORIGINAL_FORMAT_COLUMNS.extend(MONTHS_LIST)
    ORIGINAL_FORMAT_COLUMNS.extend([ORIGINAL_YEARLY_RATE_COLUMN])

    def __init__(self):
        pass

    def getYearTitle(self):
        return OriginalFormatConstants.ORIGINAL_YEAR_COLUMN

    def getYearlyInterestRateTitle(self):
        return OriginalFormatConstants.ORIGINAL_YEARLY_RATE_COLUMN

    def getMonthsList(self):
        return OriginalFormatConstants.MONTHS_LIST

    def getColumnsTitleList(self):
        return OriginalFormatConstants.ORIGINAL_FORMAT_COLUMNS


class StackedFormatConstants:

    # Contants related to the "Stacked" dataframe format (3 columns)
    STACKED_YEAR_COLUMN = "Ano"
    STACKED_MONTH_COLUMN = "Mês"
    STACKED_ADJUSTED_DATE_COLUMN = "Data Ajustada"
    STACKED_MONTHLY_INTEREST_COLUMN = "Taxa Mensal"
    STACKED_FORMAT_COLUMNS = [
        STACKED_YEAR_COLUMN,
        STACKED_MONTH_COLUMN,
        STACKED_ADJUSTED_DATE_COLUMN,
        STACKED_MONTHLY_INTEREST_COLUMN,
    ]

    def __init__(self):
        pass

    def getYearTitle(self):
        return StackedFormatConstants.STACKED_YEAR_COLUMN

    def getMonthTitle(self):
        return StackedFormatConstants.STACKED_MONTH_COLUMN

    def getAdjustedDateTitle(self):
        return StackedFormatConstants.STACKED_ADJUSTED_DATE_COLUMN

    def getInterestTitle(self):
        return StackedFormatConstants.STACKED_MONTHLY_INTEREST_COLUMN

    def getColumnsTitleList(self):
        return StackedFormatConstants.STACKED_FORMAT_COLUMNS


class IndexerManager:

    """
    This class is useful to manipulate the 'indexer' Excel files, in order to provide information
    related to some Economic Indexers (such as IPCA, etc).

    The 'interest rate' data (%) imported by this class is inputed in the following format:
    -  0.62% --> 0.62
    - 10.51% --> 10.51

    The files shall be located in the 'indexer_lib' sub folder.

    Arguments:
    - FileName: the name of the Excel file (example: 'IPCA.xlsx')
    """

    # General contants related to the Indexer Manager
    MODULE_PATH = __file__.replace(r"\indexer_manager.py", "")
    EXCEL_DATA_FOLDER_NAME = r"data"
    EXCEL_DATA_PATH = MODULE_PATH + r"\\" + EXCEL_DATA_FOLDER_NAME

    def __init__(self, FileName, day=1):
        self.extended_value_mode = False
        self.__createConstantObjects()
        self.__createPeriodVariables(day)
        self.__createFileVariables(FileName)
        self.__createDataframes()
        self.__divideInterestValuesPer100()
        self.__setInitialFinalPeriods()
        self.__setValuesToYearlyRateColumn()

    """
    Private methods
    """

    def __createConstantObjects(self):
        self.__OriginalConstants = OriginalFormatConstants()
        self.__StackedConstants = StackedFormatConstants()

    def __createPeriodVariables(self, day):
        self.__MonthsList = self.__OriginalConstants.getMonthsList()
        self.__MonthsIndexList = range(1, 13)
        self.__YearsList = []
        self.__Day = day

    def __createFileVariables(self, FileName):
        self.__FileName = FileName
        self.__FilePath = IndexerManager.EXCEL_DATA_PATH
        self.__File = self.__FilePath + r"\\" + self.__FileName

    def __setOriginalColumnFormat(self, df):
        fdf = df[self.__OriginalConstants.getColumnsTitleList()]
        fdf = fdf.sort_values(by=[self.__OriginalConstants.getYearTitle()])
        return fdf

    def __getAdjustedDateList(self, year):
        year_string = str(year)
        day_string = str(self.__Day)
        adjusted_date_list = []
        for month_index in self.__MonthsIndexList:
            month_string = str(month_index)
            adjusted_date_string = year_string + "/" + month_string + "/" + day_string
            adjusted_date_list.append(
                datetime.strptime(adjusted_date_string, "%Y/%m/%d")
            )
        return adjusted_date_list

    def __createStackedColumnsLists(self, original_formated_dataframe):
        year_column_list = []
        month_column_list = []
        adjusted_date_column_list = []
        interest_rate_column_list = []
        # Iterate over each line of the original dataframe to create a stacked dataframe
        for line_data_row in original_formated_dataframe.itertuples(index=False):
            # line_data_row_list[0]: year
            # line_data_row_list[1-12]: the 12 months
            line_data_row_list = list(line_data_row)
            self.__YearsList.append(line_data_row_list[0])
            years = [line_data_row_list[0]] * 12
            months = self.__MonthsList
            year_column_list.extend(years)
            month_column_list.extend(months)
            adjusted_date_column_list.extend(
                self.__getAdjustedDateList(line_data_row_list[0])
            )
            interest_rate_column_list.extend(line_data_row_list[1:13])
        return (
            year_column_list,
            month_column_list,
            adjusted_date_column_list,
            interest_rate_column_list,
        )

    def __createStackedDataframe(
        self,
        year_column_list,
        month_column_list,
        adjusted_date_column_list,
        interest_rate_column_list,
    ):
        stack_formated_dictionary = {}
        stack_formated_dictionary[
            self.__StackedConstants.getYearTitle()
        ] = year_column_list
        stack_formated_dictionary[
            self.__StackedConstants.getMonthTitle()
        ] = month_column_list
        stack_formated_dictionary[
            self.__StackedConstants.getAdjustedDateTitle()
        ] = adjusted_date_column_list
        stack_formated_dictionary[
            self.__StackedConstants.getInterestTitle()
        ] = interest_rate_column_list
        stack_formated_dataframe = pd.DataFrame(stack_formated_dictionary)
        stack_formated_dataframe = stack_formated_dataframe.fillna(0.0)
        return stack_formated_dataframe

    def __setStackedColumnFormat(self, original_formated_dataframe):
        (
            year_column_list,
            month_column_list,
            adjusted_date_column_list,
            interest_rate_column_list,
        ) = self.__createStackedColumnsLists(original_formated_dataframe)
        stack_formated_dataframe = self.__createStackedDataframe(
            year_column_list,
            month_column_list,
            adjusted_date_column_list,
            interest_rate_column_list,
        )
        return stack_formated_dataframe

    def __addYearlyRateColumnToOriginalDF(self):
        empty_column_list = [""] * len(self.__OriginalDataframe)
        column_position = len(OriginalFormatConstants.ORIGINAL_FORMAT_COLUMNS) - 1
        self.__OriginalDataframe.insert(
            column_position,
            OriginalFormatConstants.ORIGINAL_YEARLY_RATE_COLUMN,
            empty_column_list,
            True,
        )

    def _getYearMonthDay(self, date, defaultDay=None):
        month = date.month
        year = date.year
        if defaultDay:
            day = defaultDay
        else:
            day = date.day
        return year, month, day

    def _getDate(self, year, month, day):
        string_list = [str(year), str(month), str(day)]
        date_str = "-".join(string_list)
        return datetime.strptime(date_str, "%Y-%m-%d")

    def _getDateFromString(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    def __getLastLineDataframe(self, df):
        df = df.iloc[-1:]
        for index, row in df.iterrows():
            index = index
        return df, index

    def __getOneLineParams(self, one_line_df):
        for index, row in one_line_df.iterrows():
            year = int(row[self.__StackedConstants.getYearTitle()])
            month_str = str(row[self.__StackedConstants.getMonthTitle()])
            month = self.__MonthsList.index(month_str) + 1
            datestr = str(row[self.__StackedConstants.getAdjustedDateTitle()])
            date = self._getDateFromString(datestr)
            rate = float(row[self.__StackedConstants.getInterestTitle()])
        return year, month, date, rate

    def __getNextMonthDate(self, date):
        next_date = date + relativedelta(months=+1)
        year, month, day = self._getYearMonthDay(next_date)
        date_string = self._getDate(year, month, day)
        return year, month, day, next_date, date_string

    def __addNewLine(self, extended_df, syear, smonth, sdatestr, srate):
        month_str = self.__MonthsList[smonth - 1]
        line_df = pd.DataFrame()
        line_df[self.__StackedConstants.getYearTitle()] = [syear]
        line_df[self.__StackedConstants.getMonthTitle()] = [month_str]
        line_df[self.__StackedConstants.getAdjustedDateTitle()] = [sdatestr]
        line_df[self.__StackedConstants.getInterestTitle()] = [srate]
        extended_df = pd.concat(
            [extended_df, line_df],
            ignore_index=True,
            sort=False,
        )
        return extended_df

    def __filterNotValidLines(self, extended_df, line_index):
        return extended_df[extended_df.index <= line_index]

    def __setExtendedDataframe(self, stacked_df):
        # Select the last line with 'rate != 0.0'
        rate_col = self.__StackedConstants.getInterestTitle()
        filtered_df = stacked_df.loc[stacked_df[rate_col] != 0.0000]
        last_valid_line, last_vl_idx = self.__getLastLineDataframe(filtered_df)

        # Get the parameters of the 'last_valid_line'
        lyear, lmonth, ldate, lrate = self.__getOneLineParams(last_valid_line)

        # Create the extended stacked dataframe
        extended_df = stacked_df.copy()
        extended_df = self.__filterNotValidLines(extended_df, last_vl_idx)

        # Set the adjusted current date variables (day=1)
        cur_date = datetime.today()
        cyear, cmonth, cday = self._getYearMonthDay(cur_date, defaultDay=1)
        cdate = self._getDate(cyear, cmonth, cday)
        cdate_str = self._getDate(cyear, cmonth, cday)

        # Set the last line variables related to the extended stacked dataframe
        last_sline, last_sline_idx = self.__getLastLineDataframe(extended_df)
        syear, smonth, sdate, srate = self.__getOneLineParams(last_sline)

        # Extend the 'extended_df'
        while sdate <= cdate:
            # 'extended_df' is fully updated with data from web
            if (syear == cyear) and (smonth == cmonth):
                break
            # 'extended_df' is missing updated data from web
            else:
                self.extended_value_mode = True
                param_tuple = self.__getNextMonthDate(sdate)
                syear, smonth, sday, sdate, sdatestr = param_tuple
                extended_df = self.__addNewLine(
                    extended_df,
                    syear,
                    smonth,
                    sdatestr,
                    lrate,
                )
        return extended_df

    def __createDataframes(self):
        self.__OriginalDataframe = pd.read_excel(self.__File)
        self.__addYearlyRateColumnToOriginalDF()
        self.__OriginalDataframe = self.__setOriginalColumnFormat(
            self.__OriginalDataframe
        )
        self.__StackedDataframe = self.__setStackedColumnFormat(
            self.__OriginalDataframe
        )
        self.__ExtendedStackedDataframe = self.__setExtendedDataframe(
            self.__StackedDataframe
        )

    def __divideInterestValuesPer100(self):
        for month in self.__OriginalConstants.getMonthsList():
            self.__OriginalDataframe[month] /= 100
        rate_col = self.__StackedConstants.getInterestTitle()
        self.__StackedDataframe[rate_col] /= 100
        self.__ExtendedStackedDataframe[rate_col] /= 100

    def __setInitialFinalPeriods(self):
        year_list = list(
            self.__StackedDataframe[self.__StackedConstants.getYearTitle()]
        )
        self.__InitialYear = year_list[0]
        self.__FinalYear = year_list[-1]
        month_list = list(
            self.__StackedDataframe[self.__StackedConstants.getMonthTitle()]
        )
        self.__InitialMonth = month_list[0]
        self.__FinalMonth = month_list[-1]

    def __setValuesToYearlyRateColumn(self):
        interest_rate_list = []
        interest_calculation = InterestCalculation()
        dataframe_list = self.__OriginalDataframe.values.tolist()
        total_value = 1000.0
        for list_per_year in dataframe_list:
            rates_per_month_list = list_per_year[1:13]
            interest_rate = interest_calculation.calculateInterestRate(
                rates_per_month_list, total_value
            )
            interest_rate_list.append(interest_rate)
            interest_value_per_month = interest_calculation.calculateInterestValue(
                rates_per_month_list, total_value
            )
            total_value += interest_value_per_month
        self.__OriginalDataframe[
            self.__OriginalConstants.getYearlyInterestRateTitle()
        ] = interest_rate_list

    """
    Puclic methods
    """

    def getDataframe(self, stacked=True):
        """
        Returns the dataframe related to the data series, in 'original' or 'stacked' (default) format

        - Original Format: 13 columns ('Ano', 'Janeiro', 'Fevereiro', ..., 'Dezembro'), where:
          > 'Ano': all available years in the data series (2000, 2001, etc)
          > 'Janeiro' to 'Dezembro': the interest rates per month

        - Stacked Format: 3 columns ('Ano', 'Mês', 'Taxa Mensal'), where:
          > 'Ano': all available years in the data series (2000, 2001, etc)
          > 'Mês': all available months in the data series ('Janeiro', 'Fevereiro', etc)
          > 'Taxa Mensal': the interest rates per month
        """
        if stacked:
            return self.__StackedDataframe
        else:
            return self.__OriginalDataframe

    def getExtendedDataframe(self):
        """
        Returns the extended dataframe related to the data series, in 'stacked' format
        """
        return self.__ExtendedStackedDataframe

    def isExtendedModeEnabled(self):
        """
        Return if the spreadsheet data, related to the economic indexers, is manipulated or not.
        """
        return self.extended_value_mode

    def getFormatedDataframe(self, stacked=True):
        """
        Returns the formated dataframe related to the data series, in 'original' or 'stacked' (default) format
        """
        if stacked:
            stacked_formater = StackedIndexerFormater(self.getDataframe(stacked=True))
            formated_dataframe = stacked_formater.getFormatedDataFrame()
            return formated_dataframe
        else:
            original_formater = OriginalIndexerFormater(
                self.getDataframe(stacked=False)
            )
            formated_dataframe = original_formater.getFormatedDataFrame()
            return formated_dataframe

    def getFileName(self):
        """
        Returns the file name from where the data series comes from
        """
        return self.__FileName

    def getFilePath(self):
        """
        Returns the file path from where the data series comes from
        """
        return self.__FilePath

    def getSeriesInitialPeriod(self, month_as_string=True):
        """
        Returns the initial period (Year and Month) related to the available data series

        If 'month_as_string' is 'True', return 'Janeiro', 'Fevereiro', etc.
        If 'month_as_string' is 'False', return '1', '2', etc.
        """
        if month_as_string:
            return self.__InitialYear, self.__InitialMonth
        else:
            return self.__InitialYear, (
                self.__MonthsList.index(self.__InitialMonth) + 1
            )

    def getSeriesFinalPeriod(self, month_as_string=True):
        """
        Returns the final period (Year and Month) related to the available data series
        """
        if month_as_string:
            return self.__FinalYear, self.__FinalMonth
        else:
            return self.__FinalYear, (self.__MonthsList.index(self.__FinalMonth) + 1)

    def getMonthsList(self):
        """
        Returns a list of months as strings (Janeiro, Fevereiro, etc.)
        """
        return self.__MonthsList

    def getYearsList(self):
        """
        Returns a list of years related to the Initial and Final periods of the data series
        """
        return self.__YearsList
