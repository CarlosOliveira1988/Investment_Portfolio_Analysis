from gui_lib.treeview.treeview_format import (
    CurencyColumnType,
    DateColumnType,
    FloatColumnType,
    NonRequiredStringColumnType,
    PercentageColumnType,
    RequiredStringColumnType,
)


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
        self.Market = RequiredStringColumnType("Mercado")
        self.Ticker = RequiredStringColumnType("Ticker")
        self.Operation = RequiredStringColumnType("Operação")
        self.Date = DateColumnType("Data")
        self.Profitability = PercentageColumnType("Rentabilidade Contratada")
        self.Index = NonRequiredStringColumnType("Indexador")
        self.DueDate = DateColumnType("Vencimento")
        self.Quantity = FloatColumnType("Quantidade")
        self.UnitPrice = CurencyColumnType("Preço Unitário")
        self.TotalPrice = CurencyColumnType("Preço Total")
        self.Fees = CurencyColumnType("Taxas")
        self.IncomeTax = CurencyColumnType("IR")
        self.Divided = CurencyColumnType("Dividendos")
        self.Jcp = CurencyColumnType("JCP")
        self.TotalCost = CurencyColumnType("Custo Total")
        self.Notes = NonRequiredStringColumnType("Notas")
        self.ColumnsVariableList = []

    def __appendColumnsVariableList(self):
        self.ColumnsVariableList.append("Market")
        self.ColumnsVariableList.append("Ticker")
        self.ColumnsVariableList.append("Operation")
        self.ColumnsVariableList.append("Date")
        self.ColumnsVariableList.append("Profitability")
        self.ColumnsVariableList.append("Index")
        self.ColumnsVariableList.append("DueDate")
        self.ColumnsVariableList.append("Quantity")
        self.ColumnsVariableList.append("UnitPrice")
        self.ColumnsVariableList.append("TotalPrice")
        self.ColumnsVariableList.append("Fees")
        self.ColumnsVariableList.append("IncomeTax")
        self.ColumnsVariableList.append("Divided")
        self.ColumnsVariableList.append("Jcp")
        self.ColumnsVariableList.append("TotalCost")
        self.ColumnsVariableList.append("Notes")

    def __fillNaValues(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = PortfolioFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.fillNaDataFrameColumnValues(self.FormatedPortolioDataFrame)

    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = PortfolioFormater.__getattribute__(
                self, column_variable_string
            )
            columns_title_list.append(column_type.getTitle())
        self.FormatedPortolioDataFrame = self.FormatedPortolioDataFrame[
            columns_title_list
        ]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = PortfolioFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.formatDataFrameColumnValues(self.FormatedPortolioDataFrame)

    """
    Public methods
    """

    def getColumnsTitleList(self):
        return list(self.FormatedPortolioDataFrame)

    def getFormatedPortolioDataFrame(self):
        return self.FormatedPortolioDataFrame


class VariableIncomesFormater:
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
        self.Market = RequiredStringColumnType("Mercado")
        self.Ticker = RequiredStringColumnType("Ticker")
        self.Quantity = FloatColumnType("Quantidade")
        self.MeanPrice = CurencyColumnType("Preço médio")
        self.Quotation = CurencyColumnType("Cotação")
        self.PaidPrice = CurencyColumnType("Preço pago")
        self.MarketPrice = CurencyColumnType("Preço mercado")
        self.DeltaPrice = CurencyColumnType("Preço mercado-pago")
        self.RentDelta = PercentageColumnType("Rentabilidade mercado-pago")
        self.Dividend = CurencyColumnType("Proventos")
        self.NetValue = CurencyColumnType("Resultado liquido")
        self.RentNetValue = PercentageColumnType("Rentabilidade liquida")
        self.WalletPercentage = PercentageColumnType("Porcentagem carteira")
        self.ColumnsVariableList = []

    def __appendColumnsVariableList(self):
        self.ColumnsVariableList.append("Market")
        self.ColumnsVariableList.append("Ticker")
        self.ColumnsVariableList.append("Quantity")
        self.ColumnsVariableList.append("MeanPrice")
        self.ColumnsVariableList.append("Quotation")
        self.ColumnsVariableList.append("PaidPrice")
        self.ColumnsVariableList.append("MarketPrice")
        self.ColumnsVariableList.append("DeltaPrice")
        self.ColumnsVariableList.append("RentDelta")
        self.ColumnsVariableList.append("Dividend")
        self.ColumnsVariableList.append("NetValue")
        self.ColumnsVariableList.append("RentNetValue")
        self.ColumnsVariableList.append("WalletPercentage")

    def __fillNaValues(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = VariableIncomesFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.fillNaDataFrameColumnValues(self.FormatedPortolioDataFrame)

    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = VariableIncomesFormater.__getattribute__(
                self, column_variable_string
            )
            columns_title_list.append(column_type.getTitle())
        self.FormatedPortolioDataFrame = self.FormatedPortolioDataFrame[
            columns_title_list
        ]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = VariableIncomesFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.formatDataFrameColumnValues(self.FormatedPortolioDataFrame)

    """
    Public methods
    """

    def getColumnsTitleList(self):
        return list(self.FormatedPortolioDataFrame)

    def getFormatedPortolioDataFrame(self):
        return self.FormatedPortolioDataFrame


class TreasuriesFormater:
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
        self.Ticker = RequiredStringColumnType("Ticker")
        self.Indexer = RequiredStringColumnType("Indexador")
        self.Quantity = FloatColumnType("Quantidade")
        self.MeanPrice = CurencyColumnType("Preço médio")
        self.Quotation = CurencyColumnType("Cotação")
        self.BuyPrice = CurencyColumnType("Preço pago")
        self.MarketPrice = CurencyColumnType("Preço mercado")
        self.DeltaPrice = CurencyColumnType("Preço mercado-pago")
        self.RentDelta = PercentageColumnType("Rentabilidade mercado-pago")
        self.Dividend = CurencyColumnType("Proventos")
        self.NetValue = CurencyColumnType("Resultado liquido")
        self.RentNetValue = PercentageColumnType("Rentabilidade liquida")
        self.WalletPercentage = PercentageColumnType("Porcentagem carteira")
        self.ColumnsVariableList = []

    def __appendColumnsVariableList(self):
        self.ColumnsVariableList.append("Ticker")
        self.ColumnsVariableList.append("Indexer")
        self.ColumnsVariableList.append("Quantity")
        self.ColumnsVariableList.append("MeanPrice")
        self.ColumnsVariableList.append("Quotation")
        self.ColumnsVariableList.append("BuyPrice")
        self.ColumnsVariableList.append("MarketPrice")
        self.ColumnsVariableList.append("DeltaPrice")
        self.ColumnsVariableList.append("RentDelta")
        self.ColumnsVariableList.append("Dividend")
        self.ColumnsVariableList.append("NetValue")
        self.ColumnsVariableList.append("RentNetValue")
        self.ColumnsVariableList.append("WalletPercentage")

    def __fillNaValues(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = TreasuriesFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.fillNaDataFrameColumnValues(self.FormatedPortolioDataFrame)

    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = TreasuriesFormater.__getattribute__(
                self, column_variable_string
            )
            columns_title_list.append(column_type.getTitle())
        self.FormatedPortolioDataFrame = self.FormatedPortolioDataFrame[
            columns_title_list
        ]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = TreasuriesFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.formatDataFrameColumnValues(self.FormatedPortolioDataFrame)

    """
    Public methods
    """

    def getColumnsTitleList(self):
        return list(self.FormatedPortolioDataFrame)

    def getFormatedPortolioDataFrame(self):
        return self.FormatedPortolioDataFrame
