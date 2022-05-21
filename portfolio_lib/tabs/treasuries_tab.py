"""File to handle the Treasuries TAB."""

from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from portfolio_lib.portfolio_formater import TreasuriesFormater
from portfolio_lib.tabs.tab_viewer import TabViewerInterface
from widget_lib.tab_viewer import TabViewerWidget


class TreasuriesTabInterface(TabViewerInterface):
    """TreasuriesTabInterface to work together with PortfolioViewerWidget."""

    def __init__(self, addNewTabMethod):
        """Create the TreasuriesTabInterface object."""
        super().__init__()
        self.addNewTabMethod = addNewTabMethod
        self.formatter = None
        self.treasuries_treeview = None
        self.TreasuriesTab = None

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
        self.formatter = TreasuriesFormater(dataframe)
        formatted_df = self.formatter.getFormattedDataFrame()
        self.treasuries_treeview = ResizableTreeviewPandas(formatted_df)
        self.treasuries_treeview.showPandas(resize_per_contents=False)
        self.TreasuriesTab = TabViewerWidget(
            [self.treasuries_treeview],
            "Tesouro Direto",
            spacing=Window.DEFAULT_BORDER_SIZE,
        )
        self.TabIndex = self.addNewTabMethod(self.TreasuriesTab)
        self.onChangeAction()

    def clearData(self):
        """Clear the data table."""
        self.treasuries_treeview.clearData()

    def updateData(self, dataframe):
        """Update the data table."""
        dataframe = self.__addTotalLine(dataframe)
        self.formatter = TreasuriesFormater(dataframe)
        formatted_df = self.formatter.getFormattedDataFrame()
        self.treasuries_treeview.clearData()
        self.treasuries_treeview.setDataframe(formatted_df)
        self.treasuries_treeview.showPandas(resize_per_contents=False)
        self.onChangeAction()

    def onChangeAction(self):
        """Execute during the onChange method."""
        self.treasuries_treeview.resizeColumnsToContents()

    def getTabIndex(self):
        """Return the Tab index."""
        return self.TabIndex
