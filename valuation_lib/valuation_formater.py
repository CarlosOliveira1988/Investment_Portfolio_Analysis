"""This file has methods to format valuation tables."""

from gui_lib.treeview.treeview_format import (
    CurencyColumnType,
    DateColumnType,
    FloatColumnType,
    PercentageColumnType,
    RequiredStringColumnType,
)


class FundamentalAnalysisFormater:
    """This class is useful to format fundamentalist dataFrames.

    The following attributes are controlled by this class:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - dataframe: the fundamentalist pandas dataframe
    """

    def __init__(self, dataframe):
        """Create the formatter objct."""
        self.__assignColumnVariables()
        self.__appendColumnsVariableList()
        self.FormatedDataFrame = dataframe
        self.__setColumnOrder()
        self.__fillNaValues()
        self.__format()

    """
    Private methods
    """

    def __assignColumnVariables(self):
        self.Ticker = RequiredStringColumnType("Ticker")
        self.Sector = RequiredStringColumnType("Setor")
        self.Price = CurencyColumnType("Preço atual")
        self.VPA = CurencyColumnType("VPA")
        self.LPA = CurencyColumnType("LPA")
        self.PL = FloatColumnType("P/L")
        self.PVPA = PercentageColumnType("P/VPA")
        self.DividendYield = PercentageColumnType("Dividend Yield")
        self.Dividend = CurencyColumnType("Dividendos 12-meses")
        self.ExDividend = DateColumnType("Data ex-dividendos")
        self.LastDividend = DateColumnType("Data último-dividendo")
        self.LastSplit = DateColumnType("Data último-split")

    def __appendColumnsVariableList(self):
        self.ColumnsVariableList = list(self.__dict__)

    def __fillNaValues(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = FundamentalAnalysisFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.fillNaDataFrameColumnValues(self.FormatedDataFrame)

    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = FundamentalAnalysisFormater.__getattribute__(
                self, column_variable_string
            )
            columns_title_list.append(column_type.getTitle())
        self.FormatedDataFrame = self.FormatedDataFrame[columns_title_list]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = FundamentalAnalysisFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.formatDataFrameColumnValues(self.FormatedDataFrame)

    """
    Public methods
    """

    def getColumnsTitleList(self):
        """Get the titles list."""
        return list(self.FormatedDataFrame)

    def getFormatedDataFrame(self):
        """Get the formated dataframe."""
        return self.FormatedDataFrame
