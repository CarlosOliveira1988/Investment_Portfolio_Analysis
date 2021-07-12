from indexer_manager import IndexerManager
from treeview_format import RequiredStringColumnType
from treeview_format import PercentageColumnType


class StackedIndexerFormater:
    """
    This class is useful to format Economic Indexers as "Stacked Format" by setting:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - data_frame: the portfolio pandas dataframe
    """
    def __init__(self, data_frame):
        self.__FormatedDataFrame = data_frame
        self.__assignColumnVariables()
        self.__appendColumnsVariableList()
        self.__setColumnOrder()
        self.__fillNaValues()
        self.__format()

    """
    Private methods
    """
    def __assignColumnVariables(self):
        self.Year = RequiredStringColumnType(IndexerManager.STACKED_YEAR_COLUMN)
        self.Month = RequiredStringColumnType(IndexerManager.STACKED_MONTH_COLUMN)
        self.InterestRate = PercentageColumnType(IndexerManager.STACKED_MONTHLY_INTEREST_COLUMN)
        self.ColumnsVariableList = []

    def __appendColumnsVariableList(self):
        self.ColumnsVariableList.append('Year')
        self.ColumnsVariableList.append('Month')
        self.ColumnsVariableList.append('InterestRate')

    def __fillNaValues(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = StackedIndexerFormater.__getattribute__(self, column_variable_string)
            column_type.fillNaDataFrameColumnValues(self.__FormatedDataFrame)
    
    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = StackedIndexerFormater.__getattribute__(self, column_variable_string)
            columns_title_list.append(column_type.getTitle())
        self.__FormatedDataFrame = self.__FormatedDataFrame[columns_title_list]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = StackedIndexerFormater.__getattribute__(self, column_variable_string)
            column_type.formatDataFrameColumnValues(self.__FormatedDataFrame)

    """
    Public methods
    """
    def getColumnsTitleList(self):
        return list(self.__FormatedDataFrame)
    
    def getFormatedDataFrame(self):
        return self.__FormatedDataFrame


class OriginalIndexerFormater:
    """
    This class is useful to format Economic Indexers as "Original Format" by setting:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - data_frame: the portfolio pandas dataframe
    """
    def __init__(self, data_frame):
        self.__FormatedDataFrame = data_frame
        self.__assignColumnVariables()
        self.__appendColumnsVariableList()
        self.__setColumnOrder()
        self.__fillNaValues()
        self.__format()

    """
    Private methods
    """
    def __assignColumnVariables(self):
        self.Year = RequiredStringColumnType(IndexerManager.ORIGINAL_YEAR_COLUMN)
        self.January = PercentageColumnType(IndexerManager.MONTHS_LIST[0])
        self.February = PercentageColumnType(IndexerManager.MONTHS_LIST[1])
        self.March = PercentageColumnType(IndexerManager.MONTHS_LIST[2])
        self.April = PercentageColumnType(IndexerManager.MONTHS_LIST[3])
        self.May = PercentageColumnType(IndexerManager.MONTHS_LIST[4])
        self.June = PercentageColumnType(IndexerManager.MONTHS_LIST[5])
        self.July = PercentageColumnType(IndexerManager.MONTHS_LIST[6])
        self.August = PercentageColumnType(IndexerManager.MONTHS_LIST[7])
        self.September = PercentageColumnType(IndexerManager.MONTHS_LIST[8])
        self.October = PercentageColumnType(IndexerManager.MONTHS_LIST[9])
        self.November = PercentageColumnType(IndexerManager.MONTHS_LIST[10])
        self.December = PercentageColumnType(IndexerManager.MONTHS_LIST[11])
        self.ColumnsVariableList = []

    def __appendColumnsVariableList(self):
        self.ColumnsVariableList.append('Year')
        self.ColumnsVariableList.append('January')
        self.ColumnsVariableList.append('February')
        self.ColumnsVariableList.append('March')
        self.ColumnsVariableList.append('April')
        self.ColumnsVariableList.append('May')
        self.ColumnsVariableList.append('June')
        self.ColumnsVariableList.append('July')
        self.ColumnsVariableList.append('August')
        self.ColumnsVariableList.append('September')
        self.ColumnsVariableList.append('October')
        self.ColumnsVariableList.append('November')
        self.ColumnsVariableList.append('December')

    def __fillNaValues(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = OriginalIndexerFormater.__getattribute__(self, column_variable_string)
            column_type.fillNaDataFrameColumnValues(self.__FormatedDataFrame)
    
    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = OriginalIndexerFormater.__getattribute__(self, column_variable_string)
            columns_title_list.append(column_type.getTitle())
        self.__FormatedDataFrame = self.__FormatedDataFrame[columns_title_list]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = OriginalIndexerFormater.__getattribute__(self, column_variable_string)
            column_type.formatDataFrameColumnValues(self.__FormatedDataFrame)

    """
    Public methods
    """
    def getColumnsTitleList(self):
        return list(self.__FormatedDataFrame)
    
    def getFormatedDataFrame(self):
        return self.__FormatedDataFrame
