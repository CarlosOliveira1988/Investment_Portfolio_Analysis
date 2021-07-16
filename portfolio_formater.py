from treeview_format import RequiredStringColumnType
from treeview_format import NonRequiredStringColumnType
from treeview_format import DateColumnType
from treeview_format import PercentageColumnType
from treeview_format import FloatColumnType
from treeview_format import CurencyColumnType


class PortfolioFormater:
    """
    This class is useful to format Portfolio DataFrames by setting:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - portfolio_data_frame: the portfolio pandas dataframe
    """
    def __init__(self, portfolio_data_frame):
        self.FormatedPortolioDataFrame = portfolio_data_frame
        self.__assignColumnVariables()
        self.__appendColumnsVariableList()
        self.__setColumnOrder()
        self.__fillNaValues()
        self.__format()

    """
    Private methods
    """
    def __assignColumnVariables(self):
        self.Market = RequiredStringColumnType('Mercado')
        self.Ticker = RequiredStringColumnType('Ticker')
        self.Operation = RequiredStringColumnType('Operação')
        self.Date = DateColumnType('Data')
        self.Profitability = PercentageColumnType('Rentabilidade Contratada')
        self.Index = NonRequiredStringColumnType('Indexador')
        self.DueDate = DateColumnType('Vencimento')
        self.Quantity = FloatColumnType('Quantidade')
        self.UnitPrice = CurencyColumnType('Preço Unitário')
        self.TotalPrice = CurencyColumnType('Preço Total')
        self.Fees = CurencyColumnType('Taxas')
        self.IncomeTax = CurencyColumnType('IR')
        self.Divided = CurencyColumnType('Dividendos')
        self.Jcp = CurencyColumnType('JCP')
        self.TotalCost = CurencyColumnType('Custo Total')
        self.Notes = NonRequiredStringColumnType('Notas')
        self.ColumnsVariableList = []

    def __appendColumnsVariableList(self):
        self.ColumnsVariableList.append('Market')
        self.ColumnsVariableList.append('Ticker')
        self.ColumnsVariableList.append('Operation')
        self.ColumnsVariableList.append('Date')
        self.ColumnsVariableList.append('Profitability')
        self.ColumnsVariableList.append('Index')
        self.ColumnsVariableList.append('DueDate')
        self.ColumnsVariableList.append('Quantity')
        self.ColumnsVariableList.append('UnitPrice')
        self.ColumnsVariableList.append('TotalPrice')
        self.ColumnsVariableList.append('Fees')
        self.ColumnsVariableList.append('IncomeTax')
        self.ColumnsVariableList.append('Divided')
        self.ColumnsVariableList.append('Jcp')
        self.ColumnsVariableList.append('TotalCost')
        self.ColumnsVariableList.append('Notes')

    def __fillNaValues(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = PortfolioFormater.__getattribute__(self, column_variable_string)
            column_type.fillNaDataFrameColumnValues(self.FormatedPortolioDataFrame)
    
    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = PortfolioFormater.__getattribute__(self, column_variable_string)
            columns_title_list.append(column_type.getTitle())
        self.FormatedPortolioDataFrame = self.FormatedPortolioDataFrame[columns_title_list]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = PortfolioFormater.__getattribute__(self, column_variable_string)
            column_type.formatDataFrameColumnValues(self.FormatedPortolioDataFrame)

    """
    Public methods
    """
    def getColumnsTitleList(self):
        return list(self.FormatedPortolioDataFrame)
    
    def getFormatedPortolioDataFrame(self):
        return self.FormatedPortolioDataFrame