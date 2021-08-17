from datetime import datetime

import pandas as pd

from indexer_formater import OriginalIndexerFormater, StackedIndexerFormater
from interest_calculation import InterestCalculation


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
    - FileName: the name of the Excel file (example: 'IPCA mensal.xlsx')
    """

    # General contants related to the Indexer Manager
    MODULE_PATH = __file__.replace("\indexer_manager.py", "")
    EXCEL_DATA_FOLDER_NAME = "data"
    EXCEL_DATA_PATH = MODULE_PATH + "\\" + EXCEL_DATA_FOLDER_NAME

    def __init__(self, FileName, day=1):
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
        self.__File = self.__FilePath + "\\" + self.__FileName

    def __setOriginalColumnFormat(self, dataframe):
        original_formated_dataframe = dataframe[
            self.__OriginalConstants.getColumnsTitleList()
        ]
        original_formated_dataframe = original_formated_dataframe.sort_values(
            by=[self.__OriginalConstants.getYearTitle()]
        )
        return original_formated_dataframe

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

    def __createDataframes(self):
        self.__OriginalDataframe = pd.read_excel(self.__File)
        self.__addYearlyRateColumnToOriginalDF()
        self.__OriginalDataframe = self.__setOriginalColumnFormat(
            self.__OriginalDataframe
        )
        self.__StackedDataframe = self.__setStackedColumnFormat(
            self.__OriginalDataframe
        )

    def __divideInterestValuesPer100(self):
        for month in self.__OriginalConstants.getMonthsList():
            self.__OriginalDataframe[month] /= 100
        self.__StackedDataframe[self.__StackedConstants.getInterestTitle()] /= 100

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
