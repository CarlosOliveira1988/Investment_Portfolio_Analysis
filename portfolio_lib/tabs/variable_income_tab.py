"""File to handle the Variable Income TAB."""

from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from portfolio_lib.portfolio_formater import VariableIncomesFormater
from portfolio_lib.tabs.tab_viewer import TabViewerInterface
from widget_lib.tab_viewer import TabViewerWidget


class VariableTabInterface(TabViewerInterface):
    """VariableTabInterface to work together with PortfolioViewerWidget."""

    def __init__(self, addNewTabMethod):
        """Create the ExtratoTabInterface object."""
        super().__init__()
        self.addNewTabMethod = addNewTabMethod
        self.formatter = None
        self.variable_treeview = None
        self.VariableIncomeTab = None

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
            "Mercado",
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
        self.formatter = VariableIncomesFormater(dataframe)
        formatted_df = self.formatter.getFormattedDataFrame()
        self.variable_treeview = ResizableTreeviewPandas(formatted_df)
        self.variable_treeview.showPandas(resize_per_contents=False)
        self.VariableIncomeTab = TabViewerWidget(
            [self.variable_treeview],
            "Renda Variável",
            spacing=Window.DEFAULT_BORDER_SIZE,
        )
        self.TabIndex = self.addNewTabMethod(self.VariableIncomeTab)
        self.onChangeAction()

    def clearData(self):
        """Clear the data table."""
        self.variable_treeview.clearData()

    def updateData(self, dataframe):
        """Update the data table."""
        dataframe = self.__addTotalLine(dataframe)
        self.formatter = VariableIncomesFormater(dataframe)
        formatted_dataframe = self.formatter.getFormattedDataFrame()
        self.variable_treeview.clearData()
        self.variable_treeview.setDataframe(formatted_dataframe)
        self.variable_treeview.showPandas(resize_per_contents=False)
        self.onChangeAction()

    def onChangeAction(self):
        """Execute during the onChange method."""
        self.variable_treeview.resizeColumnsToContents()

    def getTabIndex(self):
        """Return the Tab index."""
        return self.TabIndex
