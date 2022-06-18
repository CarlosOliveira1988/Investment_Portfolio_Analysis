"""File to handle the Fixed Income TAB."""

from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from portfolio_lib.portfolio_formater import FixedIncomesFormater
from portfolio_lib.tabs.tab_viewer import TabViewerInterface
from widget_lib.tab_viewer import TabViewerWidget


class FixedIncomeTabInterface(TabViewerInterface):
    """FixedIncomeTabInterface to work together with PortfolioViewerWidget."""

    def __init__(self, addNewTabMethod):
        """Create the FixedIncomeTabInterface object."""
        super().__init__()
        self.addNewTabMethod = addNewTabMethod
        self.formatter = None
        self.treeview = None
        self.tab = None

    def __addTotalLine(self, dataframe):
        dataframe = self.addTotalLine(
            dataframe,
            [
                "Preço pago",
                "Preço mercado",
                "Mercado-pago",
                "Vendas parciais",
                "Taxas Adicionais",
                "IR",
                "Dividendos",
                "JCP",
                "Líquido parcial",
            ],
            "Ticker",
            [
                [
                    "Mercado-pago(%)",
                    "Preço pago",
                    "Mercado-pago",
                ],
                [
                    "Líquido parcial(%)",
                    "Preço pago",
                    "Líquido parcial",
                ],
            ],
        )
        return dataframe

    def setNewData(self, dataframe):
        """Set the data table."""
        dataframe = self.__addTotalLine(dataframe)
        self.formatter = FixedIncomesFormater(dataframe)
        formatted_df = self.formatter.getFormattedDataFrame()
        self.treeview = ResizableTreeviewPandas(formatted_df)
        self.treeview.showPandas(resize_per_contents=False)
        self.tab = TabViewerWidget(
            [self.treeview],
            "Renda Fixa",
            spacing=Window.DEFAULT_BORDER_SIZE,
        )
        self.tab_index = self.addNewTabMethod(self.tab)
        self.onChangeAction()

    def clearData(self):
        """Clear the data table."""
        self.treeview.clearData()

    def updateData(self, dataframe):
        """Update the data table."""
        dataframe = self.__addTotalLine(dataframe)
        self.formatter = FixedIncomesFormater(dataframe)
        formatted_df = self.formatter.getFormattedDataFrame()
        self.treeview.clearData()
        self.treeview.setDataframe(formatted_df)
        self.treeview.showPandas(resize_per_contents=False)
        self.onChangeAction()

    def onChangeAction(self):
        """Execute during the onChange method."""
        self.treeview.resizeColumnsToContents()

    def getTabIndex(self):
        """Return the Tab index."""
        return self.tab_index
