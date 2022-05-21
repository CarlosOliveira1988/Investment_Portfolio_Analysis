"""File to handle the Short Summary TAB."""

import pandas as pd
from gui_lib.treeview.format_applier import TreeviewFormatApplier
from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from indexer_lib.dataframe_filter import DataframeFilter
from portfolio_lib.portfolio_history import MarketInfo, OperationsHistory
from portfolio_lib.tabs.tab_viewer import TabViewerInterface
from widget_lib.tab_viewer import TabViewerWidget


class CustodyInformation:
    """Class to show data related to 'custody'."""

    def __init__(self, extrato_df):
        """Create the custody information object."""
        # Dataframe 'Extrato'
        self.extrato_df = extrato_df

        # Filtered dataframe 'Extrato'
        self.df_filter = DataframeFilter()
        self.filtered_df = self.df_filter.filterDataframePerColumn(
            self.extrato_df, "Mercado", "Custodia"
        )

        # Calculate useful values
        self.fee = self.filtered_df["Taxas"].sum()
        self.incomeTax = self.filtered_df["IR"].sum()
        self.dividend = self.filtered_df["Dividendos"].sum()
        self.jcp = self.filtered_df["JCP"].sum()

        # Calculate deposit value
        self.deposit_df = self.df_filter.filterDataframePerColumn(
            self.filtered_df, "Operação", "Transferência"
        )
        self.deposit = self.deposit_df["Preço Total"].sum()

        # Calculate rescue value
        self.rescue_df = self.df_filter.filterDataframePerColumn(
            self.filtered_df, "Operação", "Resgate"
        )
        self.rescue = self.rescue_df["Preço Total"].sum()

        # Dataframe 'Custody'
        self.cust_df = pd.DataFrame()
        self.cust_df["Mercado"] = ["Custodia"]
        self.cust_df["Taxas"] = [self.fee]
        self.cust_df["IR"] = [self.incomeTax]
        self.cust_df["Dividendos"] = [self.dividend]
        self.cust_df["JCP"] = [self.jcp]
        self.cust_df["Transferência"] = [self.deposit]
        self.cust_df["Resgate"] = [self.rescue]

        # Formatter
        self.cust_formatter = TreeviewFormatApplier()
        self.cust_formatter.setDataframe(self.cust_df)
        self.cust_formatter.setRequiredString(["Mercado"])
        self.cust_formatter.setCurrencyType(
            [
                "Taxas",
                "IR",
                "Dividendos",
                "JCP",
                "Transferência",
                "Resgate",
            ]
        )

    def getDataframe(self):
        """Return a dataframe with useful data.

        The following columns are present:
        - Mercado
        - Taxas
        - IR
        - Dividendos
        - JCP
        - Transferência
        - Resgate
        """
        return self.cust_df

    def getFormattedDataframe(self):
        """Return a formatted dataframe with useful data.

        The following columns are present:
        - Mercado
        - Taxas
        - IR
        - Dividendos
        - JCP
        - Transferência
        - Resgate
        """
        self.cust_formatter.setDataframe(self.cust_df)
        self.cust_formatter.runFormatter()
        return self.cust_formatter.getFormatedDataFrame()


class ShortSummaryTabInterface(TabViewerInterface):
    """ShortSummaryTabInterface to work together with PortfolioViewerWidget."""

    def __init__(self, addNewTabMethod):
        """Create the ShortSummaryTabInterface object."""
        super().__init__()
        self.addNewTabMethod = addNewTabMethod
        self.formatter = None
        self.mkt_info = None
        self.mkt_summary_tree = None
        self.operations_info = None
        self.operations_tree = None
        self.cust_info = None
        self.cust_summary_tree = None

    def setNewData(self, dataframe):
        """Set the data table."""
        # Treeview related to Market
        self.mkt_info = MarketInfo(dataframe)
        formatted_df = self.mkt_info.getFormattedDataframe()
        total_dataframe = self.mkt_info.getTotalFormattedDataframe()
        formatted_df = pd.concat(
            [formatted_df, total_dataframe],
            ignore_index=True,
            sort=False,
        )
        self.mkt_summary_tree = ResizableTreeviewPandas(formatted_df)
        self.mkt_summary_tree.showPandas(resize_per_contents=False)
        self.mkt_summary_tree.setMaximumHeight(9 * Window.DEFAULT_BORDER_SIZE)

        # Treeview related to Closed Operations
        self.operations_info = OperationsHistory(dataframe)
        self.operations_tree = ResizableTreeviewPandas(
            self.operations_info.getFormattedClosedOperationsDataframe(),
        )
        self.operations_tree.showPandas(resize_per_contents=True)

        # Treeview related to Custody
        self.cust_info = CustodyInformation(dataframe)
        self.cust_summary_tree = ResizableTreeviewPandas(
            self.cust_info.getFormattedDataframe(),
        )
        self.cust_summary_tree.showPandas(resize_per_contents=False)
        self.cust_summary_tree.setMaximumHeight(3 * Window.DEFAULT_BORDER_SIZE)

        # Short Summary tab
        self.SummaryTab = TabViewerWidget(
            [
                self.mkt_summary_tree,
                self.operations_tree,
                self.cust_summary_tree,
            ],
            "Resumo Extrato",
            spacing=Window.DEFAULT_BORDER_SIZE,
        )
        self.TabIndex = self.addNewTabMethod(self.SummaryTab)

    def clearData(self):
        """Clear the data table."""
        self.mkt_summary_tree.clearData()
        self.operations_tree.clearData()
        self.cust_summary_tree.clearData()

    def updateData(self, dataframe):
        """Update the data table."""
        # Treeview related to Market
        self.mkt_info = MarketInfo(dataframe)
        formatted_dataframe = self.mkt_info.getFormattedDataframe()
        total_dataframe = self.mkt_info.getTotalFormattedDataframe()
        formatted_dataframe = pd.concat(
            [formatted_dataframe, total_dataframe],
            ignore_index=True,
            sort=False,
        )
        self.mkt_summary_tree.clearData()
        self.mkt_summary_tree.setDataframe(formatted_dataframe)
        self.mkt_summary_tree.showPandas(resize_per_contents=False)

        # Treeview related to Closed Operations
        self.operations_info = OperationsHistory(dataframe)
        formatted_dataframe = (
            self.operations_info.getFormattedClosedOperationsDataframe()
        )
        self.operations_tree.clearData()
        self.operations_tree.setDataframe(formatted_dataframe)
        self.operations_tree.showPandas(resize_per_contents=True)

        # Treeview related to Custody
        self.cust_info = CustodyInformation(dataframe)
        formatted_dataframe = self.cust_info.getFormattedDataframe()
        self.cust_summary_tree.clearData()
        self.cust_summary_tree.setDataframe(formatted_dataframe)
        self.cust_summary_tree.showPandas(resize_per_contents=False)

    def onChangeAction(self):
        """Execute during the onChange method."""
        self.cust_summary_tree.resizeColumnsToTreeViewWidth()
        self.mkt_summary_tree.resizeColumnsToTreeViewWidth()

    def getTabIndex(self):
        """Return the Tab index."""
        return self.TabIndex
