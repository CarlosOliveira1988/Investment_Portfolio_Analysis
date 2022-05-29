"""File to handle the Short Summary TAB."""

import pandas as pd
from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from portfolio_lib.portfolio_history import OperationsHistory
from portfolio_lib.tabs.summary.custody_info import CustodyInformation
from portfolio_lib.tabs.summary.market_info import MarketInfo
from portfolio_lib.tabs.tab_viewer import TabViewerInterface
from widget_lib.tab_viewer import TabViewerWidget


class TableInterface:
    """Interface to deal with different summary tables."""

    def __init__(self, proportional_height=None, resize_per_contents=False):
        """Create the SummaryTableInterface object.

        Arguments:
        - proportional_height: a value related to the height of the treeview
        """
        self.dataframe = pd.DataFrame()
        self.tree = ResizableTreeviewPandas(self.dataframe)
        self.tree.showPandas(resize_per_contents=resize_per_contents)
        if proportional_height:
            height = proportional_height * Window.DEFAULT_BORDER_SIZE
            self.tree.setMaximumHeight(height)

    def getDataframe(self):
        """Return the current Dataframe object."""
        return self.dataframe

    def getTree(self):
        """Return the Treeview object."""
        return self.tree

    def resizeTree(self):
        """Resize the Treeview columns."""
        self.tree.resizeColumnsToTreeViewWidth()

    def clearData(self):
        """Clear the data table."""
        self.tree.clearData()

    def updateData(self, dataframe, resize_per_contents=False):
        """Update the data table."""
        self.dataframe = dataframe
        self.tree.clearData()
        self.tree.setDataframe(self.dataframe)
        self.tree.showPandas(resize_per_contents=resize_per_contents)


class ClosedInvestmentTable(TableInterface):
    """Table to show data related to Closed Investment."""

    def __init__(self):
        """Create the ClosedInvestmentTable object."""
        super().__init__(proportional_height=9)

    def updateTreeviewData(self, dataframe):
        """Update the Treeview data table."""
        mkt_info = MarketInfo(dataframe)
        self.updateData(mkt_info.getFullFormattedDataframe())


class DetailClosedInvestmentTable(TableInterface):
    """Table to show data related to Closed Investment."""

    def __init__(self):
        """Create the DetailClosedInvestmentTable object."""
        super().__init__(resize_per_contents=True)

    def updateTreeviewData(self, dataframe):
        """Update the Treeview data table."""
        op_info = OperationsHistory(dataframe)
        self.updateData(
            op_info.getFormattedClosedOperationsDataframe(),
            resize_per_contents=True,
        )

    def resizeTree(self):
        """Resize the Treeview columns."""
        self.tree.resizeColumnsToContents()


class CustodyTable(TableInterface):
    """Table to show data related to Custody."""

    def __init__(self):
        """Create the CustodyTable object."""
        super().__init__(proportional_height=3)

    def updateTreeviewData(self, dataframe):
        """Update the Treeview data table."""
        mkt_info = CustodyInformation(dataframe)
        self.updateData(mkt_info.getFormattedDataframe())


class ShortSummaryTabInterface(TabViewerInterface):
    """ShortSummaryTabInterface to work together with PortfolioViewerWidget.

    Basically, it has some tables to summarize the Investment History.
    """

    def __init__(self, addNewTabMethod):
        """Create the ShortSummaryTabInterface object."""
        super().__init__()

        # Tables
        self.table_list = []
        self.closed_table = self.__addTable(ClosedInvestmentTable())
        self.closed_hist_table = self.__addTable(DetailClosedInvestmentTable())
        self.custody_table = self.__addTable(CustodyTable())

        # Tab widget
        self.tab_widget, self.tab_index = self.__addTabWidget(addNewTabMethod)

    def __addTable(self, table):
        self.table_list.append(table)
        return table

    def __addTabWidget(self, addNewTabMethod):
        tab = TabViewerWidget(
            [table.getTree() for table in self.table_list],
            "Extrato Resumido",
            spacing=Window.DEFAULT_BORDER_SIZE,
        )
        tab_index = addNewTabMethod(tab)
        return tab, tab_index

    def setNewData(self, dataframe):
        """Set the data table."""
        [table.updateTreeviewData(dataframe) for table in self.table_list]

    def clearData(self):
        """Clear the data table."""
        [table.clearData() for table in self.table_list]

    def updateData(self, dataframe):
        """Update the data table."""
        [table.updateTreeviewData(dataframe) for table in self.table_list]

    def onChangeAction(self):
        """Execute during the onChange method."""
        [table.resizeTree() for table in self.table_list]

    def getTabIndex(self):
        """Return the Tab index."""
        return self.tab_index
