"""This file is useful to format the portfolio dataframe."""

from portfolio_lib.portfolio_formater import PortfolioFormater


class PortfolioViewerManager:
    """This class is useful to handle the portfolio dataframe visualization.

    Basically, it formats each column according to some 'string formats'.

    Arguments:
    - PortolioDataFrame: the portfolio pandas dataframe
    """

    def __init__(self, PortolioDataFrame):
        """Create the PortfolioViewerManager object."""
        self.PortfolioFormater = PortfolioFormater(PortolioDataFrame)
        self.FormatedDF = self.PortfolioFormater.getFormatedPortolioDataFrame()

    """
    Public methods
    """

    def getColumnsTitleList(self):
        """Return a columns title list."""
        return self.PortfolioFormater.getColumnsTitleList()

    def getColumnNonDuplicatedValuesList(self, column_header):
        """Return a list with non-duplicated values."""
        column_list = list(self.FormatedDF[column_header])
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
        """Apply some filter in the dataframe."""
        if ticker != "all":
            table = self.FormatedDF[self.FormatedDF["Ticker"] == ticker]
        if market != "all":
            table = self.FormatedDF[self.FormatedDF["Mercado"] == market]
        if dueDate != "NA":
            table = self.FormatedDF[self.FormatedDF["Vencimento"] == dueDate]
        if profitability != "NA":
            table = self.FormatedDF[
                self.FormatedDF["Rentabilidade Contratada"] == dueDate
            ]
        if index != "all":
            table = self.FormatedDF[self.FormatedDF["Indexador"] == index]
        if operation != "all":
            table = self.FormatedDF[self.FormatedDF["Operação"] == operation]
        return table

    def getFormattedDataframe(self):
        """Return a formatted dataframe."""
        return self.FormatedDF
