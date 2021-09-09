"""This file has a set of classes to display data from Portfolio."""

from gui_lib.pushbutton import StandardPushButton
from gui_lib.treeview.treeview import Treeview
from gui_lib.treeview.treeview_pandas import TreeviewPandas
from gui_lib.window import Window
from PyQt5 import QtCore, QtWidgets

from portfolio_lib.portfolio_formater import TreasuriesFormater, VariableIncomesFormater
from portfolio_lib.portfolio_investment import PorfolioInvestment
from portfolio_lib.portfolio_viewer_manager import PortfolioViewerManager


class ExpandCollapsePushButton(StandardPushButton):
    """PushButton Class used for expanding/collapsing lines in a table."""

    # Contants related to the special push button
    EXPAND_TEXT = "Expandir linhas"
    COLLAPSE_TEXT = "Retrair linhas"

    def __init__(
        self,
        CentralWidget=None,
        coordinate_X=0,
        coordinate_Y=0,
        onExpandMethod=None,
        onCollapseMethod=None,
        autosize=False,
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
        if autosize:
            super().__init__(
                title=ExpandCollapsePushButton.EXPAND_TEXT,
                onClickMethod=self.__expandCollapseAll,
            )
        else:
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


class PortfolioSummaryWidget(QtWidgets.QWidget):
    """Widget used to show Portfolio summary data."""

    EMPTY_SPACE = Window.DEFAULT_BORDER_SIZE

    def __init__(
        self,
        CentralWidget=None,
        PortfolioDataFrame=None,
        autosize=False,
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
        if autosize:
            super().__init__()
        else:
            super().__init__(CentralWidget)

        # PortolioTreeviewManager
        self.__PortfolioViewerManager = PortfolioViewerManager(
            PortfolioDataFrame,
        )

        # PortolioTreeview
        self.__PortfolioTreeview = Treeview(
            columns_title_list=self.__PortfolioViewerManager.getColumnsTitleList(),
            autosize=True,
        )
        self.__initTreeviewData()

        # ExpandCollapsePushButton
        self.__ExpandCollapsePushButton = ExpandCollapsePushButton(
            onExpandMethod=self.__expandAllLines,
            onCollapseMethod=self.__collapseAllLines,
            autosize=True,
        )
        self.__ExpandCollapsePushButton.setFixedSize((QtCore.QSize(200, 20)))
        self.__resizeColumns()

        # tab01 = QtWidgets.QWidget()
        grid_tab01 = QtWidgets.QGridLayout()
        grid_tab01.setContentsMargins(20, 20, 20, 20)
        grid_tab01.setSpacing(20)
        grid_tab01.addWidget(self.__PortfolioTreeview, 1, 0, 10, 1)
        grid_tab01.addWidget(self.__ExpandCollapsePushButton, 1, 1)
        self.setLayout(grid_tab01)

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


class PortfolioViewerWidget(QtWidgets.QTabWidget):
    """Widget used to show data related to Portfolio."""

    def __init__(self, File):
        """Create the PortfolioViewerWidget object.

        Arguments:
        - File: the Portfolio file
        """
        # Internal central widget
        super().__init__()
        spacing = Window.DEFAULT_BORDER_SIZE

        # PorfolioInvestment
        self.porfolio_investment = PorfolioInvestment(File)
        self.extrato = self.porfolio_investment.getExtrato()
        self.variable_income = self.porfolio_investment.currentPortfolio()
        self.treasuries = self.porfolio_investment.currentTesouroDireto()

        # Portfolio Summary tab
        self.PortfolioSummaryWidget = PortfolioSummaryWidget(
            PortfolioDataFrame=self.extrato,
            autosize=True,
        )
        self.tab01 = QtWidgets.QWidget()
        self.grid_tab01 = QtWidgets.QGridLayout()
        self.grid_tab01.setContentsMargins(0, 0, 0, 0)
        self.grid_tab01.setSpacing(0)
        self.grid_tab01.addWidget(self.PortfolioSummaryWidget)
        self.tab01.setLayout(self.grid_tab01)
        self.addTab(self.tab01, "Extrato")

        # Variable Incomes tab
        formatter = VariableIncomesFormater(self.variable_income)
        formatted_dataframe = formatter.getFormatedPortolioDataFrame()
        self.variable_treeview = TreeviewPandas(
            PandasDataFrame=formatted_dataframe,
            autosize=True,
        )
        self.variable_treeview.showPandas(resize_per_contents=False)
        self.tab02 = QtWidgets.QWidget()
        self.grid_tab02 = QtWidgets.QGridLayout()
        self.grid_tab02.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid_tab02.setSpacing(spacing)
        self.grid_tab02.addWidget(self.variable_treeview)
        self.tab02.setLayout(self.grid_tab02)
        self.addTab(self.tab02, "Renda Variável")

        # Treasuries tab
        formatter = TreasuriesFormater(self.treasuries)
        formatted_dataframe = formatter.getFormatedPortolioDataFrame()
        self.treasuries_treeview = TreeviewPandas(
            PandasDataFrame=formatted_dataframe,
            autosize=True,
        )
        self.treasuries_treeview.showPandas(resize_per_contents=False)
        self.tab03 = QtWidgets.QWidget()
        self.grid_tab03 = QtWidgets.QGridLayout()
        self.grid_tab03.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid_tab03.setSpacing(spacing)
        self.grid_tab03.addWidget(self.treasuries_treeview)
        self.tab03.setLayout(self.grid_tab03)
        self.addTab(self.tab03, "Tesouro Direto")

        # Connect tab event
        self.currentChanged.connect(self.onChange)

    def onChange(self, index):
        self.variable_treeview.resizeColumnsToTreeViewWidth()
        self.treasuries_treeview.resizeColumnsToTreeViewWidth()
