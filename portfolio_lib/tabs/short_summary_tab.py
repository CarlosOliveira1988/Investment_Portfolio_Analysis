"""File to handle the Short Summary TAB."""

import pandas as pd
from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from portfolio_lib.portfolio_history import OperationsHistory
from portfolio_lib.tabs.summary.custody_info import CustodyInformation
from portfolio_lib.tabs.summary.market_info import MarketInfo
from portfolio_lib.tabs.tab_viewer import TabViewerInterface
from widget_lib.tab_viewer import TabViewerWidget


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
