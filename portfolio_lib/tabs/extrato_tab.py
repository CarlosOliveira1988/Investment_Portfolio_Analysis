"""File to handle the Extrato TAB."""

from gui_lib.pushbutton import StandardPushButton
from gui_lib.treeview.treeview import ResizableTreeview
from gui_lib.window import Window
from portfolio_lib.portfolio_viewer_manager import PortfolioViewerManager
from portfolio_lib.tabs.tab_viewer import TabViewerInterface
from PyQt5 import QtCore, QtWidgets
from widget_lib.tab_viewer import TabViewerWidget


class ExpandCollapsePushButton(StandardPushButton):
    """PushButton Class used for expanding/collapsing lines in a table."""

    # Contants related to the special push button
    EXPAND_TEXT = "Expandir linhas"
    COLLAPSE_TEXT = "Retrair linhas"

    def __init__(
        self,
        onExpandMethod=None,
        onCollapseMethod=None,
    ):
        """Create the ExpandCollapsePushButton object.

        Arguments:
        - onExpandMethod: the callback method called to "expand" the lines
        - onCollapseMethod: the callback method called to "collapse" the lines
        """
        # Push button
        super().__init__(
            title=ExpandCollapsePushButton.EXPAND_TEXT,
            onClickMethod=self.__expandCollapseAll,
        )
        # Connect events
        self.__expandEvent = onExpandMethod
        self.__collapseEvent = onCollapseMethod

        # Initial state
        self.collapseAll()

    def __expandCollapseAll(self):
        if self.__IsExpandedFlag:
            self.collapseAll()
        else:
            self.expandAll()

    """
    Public methods
    """

    def expandAll(self):
        """Expand all grouped lines to a related treeview."""
        self.__IsExpandedFlag = True
        self.setText(ExpandCollapsePushButton.COLLAPSE_TEXT)
        self.__expandEvent()

    def collapseAll(self):
        """Collapse all grouped lines to a related treeview."""
        self.__IsExpandedFlag = False
        self.setText(ExpandCollapsePushButton.EXPAND_TEXT)
        self.__collapseEvent()


class ExtratoWidget(QtWidgets.QWidget):
    """Widget used to show Portfolio summary data."""

    EMPTY_SPACE = Window.DEFAULT_BORDER_SIZE

    def __init__(self, PortfolioDataFrame):
        """Create the ExtratoWidget object.

        Basically, it has a 'table' and a 'expand/collapse lines push button'.

        Arguments:
        - PortfolioDataFrame: the portfolio pandas dataframe
        """
        # Inheritance
        super().__init__()
        spacing = ExtratoWidget.EMPTY_SPACE

        # PortolioTreeviewManager
        self.__PortfolioViewerManager = PortfolioViewerManager(
            PortfolioDataFrame,
        )

        # PortolioTreeview
        self.__PortfolioTreeview = ResizableTreeview(
            self.__PortfolioViewerManager.getColumnsTitleList(),
        )
        self.__initTreeviewData()

        # ExpandCollapsePushButton
        self.__ExpandCollapsePushButton = ExpandCollapsePushButton(
            onExpandMethod=self.__expandAllLines,
            onCollapseMethod=self.__collapseAllLines,
        )
        self.__ExpandCollapsePushButton.setFixedSize(
            (
                QtCore.QSize(
                    StandardPushButton.DEFAULT_WIDTH,
                    StandardPushButton.DEFAULT_HEIGHT,
                )
            )
        )
        self.__resizeColumns()
        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(spacing, spacing, spacing, spacing)
        grid.setSpacing(spacing)
        grid.addWidget(self.__PortfolioTreeview, 1, 0, 10, 1)
        grid.addWidget(self.__ExpandCollapsePushButton, 1, 1)
        self.setLayout(grid)

    def __resizeColumns(self):
        self.__ExpandCollapsePushButton.expandAll()
        self.__PortfolioTreeview.resizeColumnsToContents()
        self.__ExpandCollapsePushButton.collapseAll()

    def __expandAllLines(self):
        self.__PortfolioTreeview.expandParentLines()

    def __collapseAllLines(self):
        self.__PortfolioTreeview.collapseParentLines()

    def __initTreeviewData(self):
        self.__insertTreeviewParentLines()
        self.__insertTreeviewChildrenLines()
        self.__PortfolioTreeview.expandParentLines()
        self.__PortfolioTreeview.resizeColumnsToContents()
        self.__PortfolioTreeview.collapseParentLines()

    def __insertTreeviewParentLines(self):
        self.TreeviewParentLinesDictionary = {}
        non_duplicated_market_list = (
            self.__PortfolioViewerManager.getColumnNonDuplicatedValuesList(
                "Mercado",
            )
        )
        for market in non_duplicated_market_list:
            parent_line = self.__PortfolioTreeview.insertParentLineItem(market)
            self.TreeviewParentLinesDictionary[market] = parent_line

    def __insertTreeviewChildrenLines(self):
        for (
            selected_market,
            market_parent_line,
        ) in self.TreeviewParentLinesDictionary.items():
            df_per_market = self.__PortfolioViewerManager.getCustomTable(
                market=selected_market
            )
            for line_data_row in df_per_market.itertuples(index=False):
                line_data_row_list = list(line_data_row)
                line_data_row_list[0] = " "
                self.__PortfolioTreeview.insertChildrenLineData(
                    market_parent_line, line_data_row_list
                )

    def clearData(self):
        """Clear the treeview data lines."""
        self.__PortfolioTreeview.clearData()

    def updateData(self, dataframe):
        """Update the treeview data lines."""
        self.__PortfolioViewerManager = PortfolioViewerManager(dataframe)
        self.__initTreeviewData()


class ExtratoTabInterface(TabViewerInterface):
    """ExtratoTabInterface to work together with PortfolioViewerWidget."""

    def __init__(self, addNewTabMethod):
        """Create the ExtratoTabInterface object."""
        super().__init__()
        self.addNewTabMethod = addNewTabMethod
        self.ExtratoWidget = None
        self.ExtratoTab = None
        self.TabIndex = None

    def setNewData(self, dataframe):
        """Set the data table."""
        self.ExtratoWidget = ExtratoWidget(dataframe)
        self.ExtratoTab = TabViewerWidget(
            [self.ExtratoWidget],
            "Extrato",
        )
        self.TabIndex = self.addNewTabMethod(self.ExtratoTab)

    def clearData(self):
        """Clear the data table."""
        self.ExtratoWidget.clearData()

    def updateData(self, dataframe):
        """Update the data table."""
        self.ExtratoWidget.updateData(dataframe)

    def getTabIndex(self):
        """Return the Tab index."""
        return self.TabIndex
