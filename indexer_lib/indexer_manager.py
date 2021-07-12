import pandas as pd
import sys


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
    FOLDER_PATH = 'Investment_Portfolio_Analysis\indexer_lib'
    MONTHS_LIST = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    # Contants related to the "Original" dataframe format (13 columns: similar to the observed in the Excel file)
    ORIGINAL_YEAR_COLUMN = 'Ano'
    ORIGINAL_FORMAT_COLUMNS = [ORIGINAL_YEAR_COLUMN]
    ORIGINAL_FORMAT_COLUMNS.extend(MONTHS_LIST)

    # Contants related to the "Stacked" dataframe format (3 columns)
    STACKED_YEAR_COLUMN = 'Ano'
    STACKED_MONTH_COLUMN = 'Mês'
    STACKED_MONTHLY_INTEREST_COLUMN = 'Taxa Mensal'
    STACKED_FORMAT_COLUMNS = [STACKED_YEAR_COLUMN, STACKED_MONTH_COLUMN, STACKED_MONTHLY_INTEREST_COLUMN]

    def __init__(self, FileName):
        self.__createPeriodVariables()
        self.__createFileVariables(FileName)
        self.__createDataframes()
        self.__divideInterestValuesPer100()
        self.__setInitialFinalPeriods()

    """
    Private methods
    """
    def __createPeriodVariables(self):
        self.__MonthsList = IndexerManager.MONTHS_LIST
        self.__YearsList = []

    def __getIndexerFilePath(self):
        indexer_file_path = None
        file_path_list = sys.path
        for path_item in file_path_list:
            if IndexerManager.FOLDER_PATH in path_item:
                indexer_file_path = path_item
        return indexer_file_path

    def __createFileVariables(self, FileName):
        self.__FileName = FileName
        self.__FilePath = self.__getIndexerFilePath()
        self.__File = self.__FilePath + '\\' + self.__FileName

    def __setOriginalColumnFormat(self, dataframe):
        original_formated_dataframe = dataframe[IndexerManager.ORIGINAL_FORMAT_COLUMNS]
        original_formated_dataframe = original_formated_dataframe.sort_values(by=[IndexerManager.ORIGINAL_YEAR_COLUMN])
        return original_formated_dataframe

    def __createStackedColumnsLists(self, original_formated_dataframe):
        year_column_list = []
        month_column_list = []
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
            interest_rate_column_list.extend(line_data_row_list[1:])
        return year_column_list, month_column_list, interest_rate_column_list

    def __createStackedDataframe(self, year_column_list, month_column_list, interest_rate_column_list):
        stack_formated_dictionary = {}
        stack_formated_dictionary[IndexerManager.STACKED_YEAR_COLUMN] = year_column_list
        stack_formated_dictionary[IndexerManager.STACKED_MONTH_COLUMN] = month_column_list
        stack_formated_dictionary[IndexerManager.STACKED_MONTHLY_INTEREST_COLUMN] = interest_rate_column_list
        stack_formated_dataframe = pd.DataFrame(stack_formated_dictionary)
        stack_formated_dataframe.dropna(subset = [IndexerManager.STACKED_MONTHLY_INTEREST_COLUMN], inplace=True)
        return stack_formated_dataframe

    def __setStackedColumnFormat(self, original_formated_dataframe):
        year_column_list, month_column_list, interest_rate_column_list = self.__createStackedColumnsLists(original_formated_dataframe)
        stack_formated_dataframe = self.__createStackedDataframe(year_column_list, month_column_list, interest_rate_column_list)
        return stack_formated_dataframe

    def __createDataframes(self):
        self.__OriginalDataframe = pd.read_excel(self.__File)
        self.__OriginalDataframe = self.__setOriginalColumnFormat(self.__OriginalDataframe)
        self.__StackedDataframe = self.__setStackedColumnFormat(self.__OriginalDataframe)
    
    def __divideInterestValuesPer100(self):
        for month in IndexerManager.MONTHS_LIST:
            self.__OriginalDataframe[month] /= 100
        self.__StackedDataframe[IndexerManager.STACKED_MONTHLY_INTEREST_COLUMN] /= 100

    def __setInitialFinalPeriods(self):
        year_list = list(self.__StackedDataframe[IndexerManager.STACKED_YEAR_COLUMN])
        self.__InitialYear = year_list[0]
        self.__FinalYear = year_list[-1]
        month_list = list(self.__StackedDataframe[IndexerManager.STACKED_MONTH_COLUMN])
        self.__InitialMonth = month_list[0]
        self.__FinalMonth = month_list[-1]

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
    
    def getFileName(self):
        """
        Returns the file name from where the data series comes from
        """
        return self.__FileName
    
    def getSeriesInitialPeriod(self, month_as_string=True):
        """
        Returns the initial period (Year and Month) related to the available data series

        If 'month_as_string' is 'True', return 'Janeiro', 'Fevereiro', etc.
        If 'month_as_string' is 'False', return '1', '2', etc.
        """
        if month_as_string:
            return self.__InitialYear, self.__InitialMonth
        else:
            return self.__InitialYear, (self.__MonthsList.index(self.__InitialMonth)+1)
    
    def getSeriesFinalPeriod(self, month_as_string=True):
        """
        Returns the final period (Year and Month) related to the available data series
        """
        if month_as_string:
            return self.__FinalYear, self.__FinalMonth
        else:
            return self.__FinalYear, (self.__MonthsList.index(self.__FinalMonth)+1)
