from portfolio_lib.portfolio_formater import PortfolioFormater


class PortfolioViewerManager:
    """
    This class is useful to handle the portfolio dataframe visualization.

    Basically, it formats each column according to a pre-defined 'string formats'.

    Arguments:
    - PortolioDataFrame: the portfolio pandas dataframe
    """

    def __init__(self, PortolioDataFrame):
        self.PortfolioFormater = PortfolioFormater(PortolioDataFrame)
        self.FormatedPortolioDataFrame = (
            self.PortfolioFormater.getFormatedPortolioDataFrame()
        )

    """
    Public methods
    """

    def getColumnsTitleList(self):
        return self.PortfolioFormater.getColumnsTitleList()

    def getColumnNonDuplicatedValuesList(self, column_header):
        column_list = list(self.FormatedPortolioDataFrame[column_header])
        column_list = list(set(column_list))
        if "NA" in column_list:
            column_list.remove("NA")
        column_list.sort()
        return column_list

    def getCustomTable(
        self,
        ticker="all",
        market="all",
        dueDate="NA",
        profitability="NA",
        index="all",
        operation="all",
    ):
        if ticker != "all":
            table = self.FormatedPortolioDataFrame[
                self.FormatedPortolioDataFrame["Ticker"] == ticker
            ]
        if market != "all":
            table = self.FormatedPortolioDataFrame[
                self.FormatedPortolioDataFrame["Mercado"] == market
            ]
        if dueDate != "NA":
            table = self.FormatedPortolioDataFrame[
                self.FormatedPortolioDataFrame["Vencimento"] == dueDate
            ]
        if profitability != "NA":
            table = self.FormatedPortolioDataFrame[
                self.FormatedPortolioDataFrame["Rentabilidade Contratada"] == dueDate
            ]
        if index != "all":
            table = self.FormatedPortolioDataFrame[
                self.FormatedPortolioDataFrame["Indexador"] == index
            ]
        if operation != "all":
            table = self.FormatedPortolioDataFrame[
                self.FormatedPortolioDataFrame["Operação"] == operation
            ]
        return table

    def getFormattedDataframe(self):
        return self.FormatedPortolioDataFrame
