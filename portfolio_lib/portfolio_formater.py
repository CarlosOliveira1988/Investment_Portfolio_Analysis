"""This file is useful to format the portfolio dataframe."""


from gui_lib.treeview.format_applier import TreeviewFormatApplier
from gui_lib.treeview.treeview_format import (
    CurencyColumnType,
    DateColumnType,
    FloatColumnType,
    NonRequiredStringColumnType,
    PercentageColumnType,
    RequiredStringColumnType,
)


class PortfolioFormater:
    """This class is useful to format Portfolio DataFrames.

    Basically, here we manipulate the dataframe to define:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - portfolio_data_frame: the portfolio pandas dataframe
    """

    def __init__(self, portfolio_data_frame):
        """Create the PortfolioFormater object."""
        self.FormatedDF = portfolio_data_frame
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
            column_type.fillNaDataFrameColumnValues(self.FormatedDF)

    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = PortfolioFormater.__getattribute__(
                self, column_variable_string
            )
            columns_title_list.append(column_type.getTitle())
        self.FormatedDF = self.FormatedDF[columns_title_list]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = PortfolioFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.formatDataFrameColumnValues(self.FormatedDF)

    """
    Public methods
    """

    def getColumnsTitleList(self):
        """Return a columns title list."""
        return list(self.FormatedDF)

    def getFormatedPortolioDataFrame(self):
        """Return the formatted dataframe."""
        return self.FormatedDF


class VariableIncomesFormater:
    """This class is useful to format Portfolio DataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - portfolio_data_frame: the portfolio pandas dataframe
    """

    def __init__(self, portfolio_data_frame):
        """Create the VariableIncomesFormater object."""
        self.FormatedDF = portfolio_data_frame
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
        self.Yield = PercentageColumnType("Dividend-Yield Ajustado")
        self.InitialDate = DateColumnType("Data Inicial")
        self.Quantity = FloatColumnType("Quantidade")
        self.MeanPrice = CurencyColumnType("Preço médio")
        self.MeanPriceFees = CurencyColumnType("Preço médio+taxas")
        self.Quotation = CurencyColumnType("Cotação")
        self.PaidPrice = CurencyColumnType("Preço pago")
        self.MarketPrice = CurencyColumnType("Preço mercado")
        self.DeltaPrice = CurencyColumnType("Mercado-pago")
        self.RentDelta = PercentageColumnType("Mercado-pago(%)")
        self.PartialSell = CurencyColumnType("Vendas parciais")
        self.Fees = CurencyColumnType("Taxas Adicionais")
        self.IncomeTax = CurencyColumnType("IR")
        self.Divided = CurencyColumnType("Dividendos")
        self.Jcp = CurencyColumnType("JCP")
        self.NetValue = CurencyColumnType("Líquido parcial")
        self.RentNetValue = PercentageColumnType("Líquido parcial(%)")
        self.WalletPercentage = PercentageColumnType("Porcentagem carteira")
        self.ColumnsVariableList = []

    def __appendColumnsVariableList(self):
        self.ColumnsVariableList.append("Market")
        self.ColumnsVariableList.append("Ticker")
        self.ColumnsVariableList.append("Yield")
        self.ColumnsVariableList.append("InitialDate")
        self.ColumnsVariableList.append("Quantity")
        self.ColumnsVariableList.append("MeanPrice")
        self.ColumnsVariableList.append("MeanPriceFees")
        self.ColumnsVariableList.append("Quotation")
        self.ColumnsVariableList.append("PaidPrice")
        self.ColumnsVariableList.append("MarketPrice")
        self.ColumnsVariableList.append("DeltaPrice")
        self.ColumnsVariableList.append("RentDelta")
        self.ColumnsVariableList.append("PartialSell")
        self.ColumnsVariableList.append("Fees")
        self.ColumnsVariableList.append("IncomeTax")
        self.ColumnsVariableList.append("Divided")
        self.ColumnsVariableList.append("Jcp")
        self.ColumnsVariableList.append("NetValue")
        self.ColumnsVariableList.append("RentNetValue")
        self.ColumnsVariableList.append("WalletPercentage")

    def __fillNaValues(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = VariableIncomesFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.fillNaDataFrameColumnValues(self.FormatedDF)

    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = VariableIncomesFormater.__getattribute__(
                self, column_variable_string
            )
            columns_title_list.append(column_type.getTitle())
        self.FormatedDF = self.FormatedDF[columns_title_list]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = VariableIncomesFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.formatDataFrameColumnValues(self.FormatedDF)

    """
    Public methods
    """

    def getColumnsTitleList(self):
        """Return a columns title list."""
        return list(self.FormatedDF)

    def getFormatedPortolioDataFrame(self):
        """Return the formatted dataframe."""
        return self.FormatedDF


class TreasuriesFormater:
    """This class is useful to format Portfolio DataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - portfolio_data_frame: the portfolio pandas dataframe
    """

    def __init__(self, portfolio_data_frame):
        """Create the TreasuriesFormater object."""
        self.FormatedDF = portfolio_data_frame
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
        self.MeanRate = PercentageColumnType("Rentabilidade-média Contratada")
        self.InitialDate = DateColumnType("Data Inicial")
        self.Quantity = FloatColumnType("Quantidade")
        self.MeanPrice = CurencyColumnType("Preço médio")
        self.MeanPriceFees = CurencyColumnType("Preço médio+taxas")
        self.Quotation = CurencyColumnType("Cotação")
        self.BuyPrice = CurencyColumnType("Preço pago")
        self.MarketPrice = CurencyColumnType("Preço mercado")
        self.DeltaPrice = CurencyColumnType("Mercado-pago")
        self.RentDelta = PercentageColumnType("Mercado-pago(%)")
        self.PartialSell = CurencyColumnType("Vendas parciais")
        self.Fees = CurencyColumnType("Taxas Adicionais")
        self.IncomeTax = CurencyColumnType("IR")
        self.Divided = CurencyColumnType("Dividendos")
        self.Jcp = CurencyColumnType("JCP")
        self.NetValue = CurencyColumnType("Líquido parcial")
        self.RentNetValue = PercentageColumnType("Líquido parcial(%)")
        self.WalletPercentage = PercentageColumnType("Porcentagem carteira")
        self.ColumnsVariableList = []

    def __appendColumnsVariableList(self):
        self.ColumnsVariableList.append("Ticker")
        self.ColumnsVariableList.append("Indexer")
        self.ColumnsVariableList.append("MeanRate")
        self.ColumnsVariableList.append("InitialDate")
        self.ColumnsVariableList.append("Quantity")
        self.ColumnsVariableList.append("MeanPrice")
        self.ColumnsVariableList.append("MeanPriceFees")
        self.ColumnsVariableList.append("Quotation")
        self.ColumnsVariableList.append("BuyPrice")
        self.ColumnsVariableList.append("MarketPrice")
        self.ColumnsVariableList.append("DeltaPrice")
        self.ColumnsVariableList.append("RentDelta")
        self.ColumnsVariableList.append("PartialSell")
        self.ColumnsVariableList.append("Fees")
        self.ColumnsVariableList.append("IncomeTax")
        self.ColumnsVariableList.append("Divided")
        self.ColumnsVariableList.append("Jcp")
        self.ColumnsVariableList.append("NetValue")
        self.ColumnsVariableList.append("RentNetValue")
        self.ColumnsVariableList.append("WalletPercentage")

    def __fillNaValues(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = TreasuriesFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.fillNaDataFrameColumnValues(self.FormatedDF)

    def __setColumnOrder(self):
        columns_title_list = []
        for column_variable_string in self.ColumnsVariableList:
            column_type = TreasuriesFormater.__getattribute__(
                self, column_variable_string
            )
            columns_title_list.append(column_type.getTitle())
        self.FormatedDF = self.FormatedDF[columns_title_list]

    def __format(self):
        for column_variable_string in self.ColumnsVariableList:
            column_type = TreasuriesFormater.__getattribute__(
                self, column_variable_string
            )
            column_type.formatDataFrameColumnValues(self.FormatedDF)

    """
    Public methods
    """

    def getColumnsTitleList(self):
        """Return a columns title list."""
        return list(self.FormatedDF)

    def getFormatedPortolioDataFrame(self):
        """Return the formatted dataframe."""
        return self.FormatedDF


class FixedIncomesFormater:
    """This class is useful to format Portfolio DataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - portfolio_data_frame: the portfolio pandas dataframe
    """

    def __init__(self, portfolio_data_frame):
        """Create the FixedIncomesFormater object."""
        self.formatter = TreeviewFormatApplier()
        self.formatter.setDataframe(portfolio_data_frame)
        self.formatter.setCurrencyType(
            [
                "Taxas Adicionais",
                "IR",
                "Dividendos",
                "JCP",
                "Líquido parcial",
                "Preço médio",
                "Preço médio+taxas",
                "Cotação",
                "Preço pago",
                "Preço mercado",
                "Mercado-pago",
                "Vendas parciais",
            ]
        )
        self.formatter.setFloatType(["Quantidade"])
        self.formatter.setDateType(["Data Inicial"])
        self.formatter.setPercentageType(
            [
                "Rentabilidade-média Contratada",
                "Mercado-pago(%)",
                "Líquido parcial(%)",
                "Porcentagem carteira",
            ]
        )
        self.formatter.setRequiredString(
            [
                "Ticker",
                "Indexador",
            ]
        )
        self.formatter.setColumnOrder(
            [
                "Ticker",
                "Indexador",
                "Rentabilidade-média Contratada",
                "Data Inicial",
                "Quantidade",
                "Preço médio",
                "Preço médio+taxas",
                "Cotação",
                "Preço pago",
                "Preço mercado",
                "Mercado-pago",
                "Mercado-pago(%)",
                "Vendas parciais",
                "Taxas Adicionais",
                "IR",
                "Dividendos",
                "JCP",
                "Líquido parcial",
                "Líquido parcial(%)",
                "Porcentagem carteira",
            ]
        )
        self.formatter.runFormatter()
        self.formatedDF = self.formatter.getFormatedDataFrame()

    """
    Public methods
    """

    def getColumnsTitleList(self):
        """Return a columns title list."""
        return list(self.formatedDF)

    def getFormatedPortolioDataFrame(self):
        """Return the formatted dataframe."""
        return self.formatedDF
