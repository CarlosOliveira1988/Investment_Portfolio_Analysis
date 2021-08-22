"""This file has a set of classes to display data from Portfolio."""

from PyQt5 import QtCore

from gui_lib.pushbutton import StandardPushButton
from gui_lib.tab import StandardTab
from gui_lib.treeview.treeview import Treeview
from gui_lib.window import Window
from portfolio_viewer_manager import PortfolioViewerManager
from widget_lib.widget_interface import WidgetInterface


class ExpandCollapsePushButton(StandardPushButton):
    """PushButton Class used for expanding/collapsing lines in a table."""

    # Contants related to the special push button
    EXPAND_TEXT = "Expandir linhas"
    COLLAPSE_TEXT = "Retrair linhas"

    def __init__(
        self,
        CentralWidget,
        coordinate_X=0,
        coordinate_Y=0,
        onExpandMethod=None,
        onCollapseMethod=None,
    ):
        """Create the ExpandCollapsePushButton object.

        Arguments:
        - CentralWidget: the widget where the push button will be placed
        - coordinate_X: the X coordinate inside the widget
        - coordinate_Y: the Y coordinate inside the widget
        - onExpandMethod: the callback method called to "expand" the lines
        - onCollapseMethod: the callback method called to "collapse" the lines
        """
        # Push button
        super().__init__(
            CentralWidget,
            ExpandCollapsePushButton.EXPAND_TEXT,
            coordinate_X=(coordinate_X),
            coordinate_Y=(coordinate_Y),
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


class PortfolioSummaryWidget(WidgetInterface):
    """Widget used to show Portfolio summary data."""

    EMPTY_SPACE = Window.DEFAULT_BORDER_SIZE

    def __init__(
        self,
        CentralWidget,
        PortfolioDataFrame,
        coordinate_X=0,
        coordinate_Y=0,
    ):
        """Create the PortfolioSummaryWidget object.

        Basically, it has a 'table' and a 'expand/collapse lines push button'.

        Arguments:
        - CentralWidget: the widget where the components will be placed
        - PortfolioDataFrame: the portfolio pandas dataframe
        - coordinate_X: the X coordinate inside the widget
        - coordinate_Y: the Y coordinate inside the widget
        """
        # Internal central widget
        super().__init__(CentralWidget)

        # PortolioTreeviewManager
        self.__PortfolioViewerManager = PortfolioViewerManager(
            PortfolioDataFrame,
        )

        # PortolioTreeview
        self.__PortfolioTreeview = Treeview(
            self,
            self.__PortfolioViewerManager.getColumnsTitleList(),
            coordinate_X=0,
            coordinate_Y=0,
            height=640,
        )
        empty_space = PortfolioSummaryWidget.EMPTY_SPACE
        self.incrementInternalWidth(
            self.__PortfolioTreeview.width() + empty_space,
        )
        self.incrementInternalHeight(
            self.__PortfolioTreeview.height() + empty_space,
        )
        self.__initTreeviewData()

        # ExpandCollapsePushButton
        self.__ExpandCollapsePushButton = ExpandCollapsePushButton(
            self,
            coordinate_X=self.getInternalWidth(),
            onExpandMethod=self.__expandAllLines,
            onCollapseMethod=self.__collapseAllLines,
        )
        self.__resizeColumns()
        self.incrementInternalWidth(self.__ExpandCollapsePushButton.width())

        # Widget dimensions
        self.setGeometry(
            QtCore.QRect(
                coordinate_X,
                coordinate_Y,
                self.getInternalWidth(),
                self.getInternalHeight(),
            )
        )

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
                self.__PortfolioViewerManager.PortfolioFormater.Market.Title,
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


class PortfolioViewerWidget(WidgetInterface):
    """Widget used to show data related to Portfolio."""

    EMPTY_SPACE = Window.DEFAULT_BORDER_SIZE

    def __init__(self, CentralWidget, portfolio_dataframe):
        """Create the PortfolioViewerWidget object.

        Arguments:
        - CentralWidget: the widget where the components will be placed
        - PortfolioDataFrame: the portfolio pandas dataframe
        """
        # Internal central widget
        super().__init__(CentralWidget)

        # Tab panel widget
        self.TabPanel = StandardTab(self)

        # PortfolioSummaryWidget tab
        tab_central_widget = self.TabPanel.addNewTab("Extrato")
        self.PortfolioSummaryWidget = PortfolioSummaryWidget(
            tab_central_widget,
            portfolio_dataframe,
            coordinate_X=PortfolioViewerWidget.EMPTY_SPACE,
            coordinate_Y=PortfolioViewerWidget.EMPTY_SPACE,
        )
        empty_space = PortfolioViewerWidget.EMPTY_SPACE
        self.incrementInternalWidth(
            self.PortfolioSummaryWidget.width() + empty_space,
        )
        self.incrementInternalHeight(
            self.PortfolioSummaryWidget.height() + empty_space,
        )

        # VariableIncomesWidget tab
        tab_central_widget = self.TabPanel.addNewTab("Renda Variável")

        # FixedIncomesWidget tab
        tab_central_widget = self.TabPanel.addNewTab("Renda Fixa")

        # TreasuriesWidget tab
        tab_central_widget = self.TabPanel.addNewTab("Tesouro Direto")

        # CustodyWidget tab
        tab_central_widget = self.TabPanel.addNewTab("Custódia")

        # Tab panel widget dimensions
        self.TabPanel.resize(
            self.getInternalWidth() + empty_space,
            self.getInternalHeight() + empty_space,
        )
        self.resize(
            self.TabPanel.width(),
            self.TabPanel.height(),
        )
