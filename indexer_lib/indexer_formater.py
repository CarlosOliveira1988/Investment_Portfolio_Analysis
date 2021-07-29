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
        from indexer_manager import StackedFormatConstants
        self.__FormatedDataFrame = data_frame
        self.__StackedConstants = StackedFormatConstants()
        self.__assignColumnVariables()
        self.__appendColumnsVariableList()
        self.__setColumnOrder()
        self.__fillNaValues()
        self.__format()

    """
    Private methods
    """
    def __assignColumnVariables(self):
        from treeview_format import RequiredStringColumnType
        from treeview_format import PercentageColumnType
        self.Year = RequiredStringColumnType(self.__StackedConstants.getYearTitle())
        self.Month = RequiredStringColumnType(self.__StackedConstants.getMonthTitle())
        self.InterestRate = PercentageColumnType(self.__StackedConstants.getInterestTitle())
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
        from indexer_manager import OriginalFormatConstants
        self.__FormatedDataFrame = data_frame
        self.__OriginalConstants = OriginalFormatConstants()
        self.__assignColumnVariables()
        self.__appendColumnsVariableList()
        self.__setColumnOrder()
        self.__fillNaValues()
        self.__format()

    """
    Private methods
    """
    def __assignColumnVariables(self):
        from treeview_format import RequiredStringColumnType
        from treeview_format import PercentageColumnType
        months_list = self.__OriginalConstants.getMonthsList()
        self.Year = RequiredStringColumnType(self.__OriginalConstants.getYearTitle())
        self.January = PercentageColumnType(months_list[0])
        self.February = PercentageColumnType(months_list[1])
        self.March = PercentageColumnType(months_list[2])
        self.April = PercentageColumnType(months_list[3])
        self.May = PercentageColumnType(months_list[4])
        self.June = PercentageColumnType(months_list[5])
        self.July = PercentageColumnType(months_list[6])
        self.August = PercentageColumnType(months_list[7])
        self.September = PercentageColumnType(months_list[8])
        self.October = PercentageColumnType(months_list[9])
        self.November = PercentageColumnType(months_list[10])
        self.December = PercentageColumnType(months_list[11])
        self.YearlyInterestRate = PercentageColumnType(self.__OriginalConstants.getYearlyInterestRateTitle())
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
        self.ColumnsVariableList.append('YearlyInterestRate')

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
