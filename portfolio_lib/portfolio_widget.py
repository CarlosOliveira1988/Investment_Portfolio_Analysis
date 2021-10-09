"""This file has a set of classes to display data from Portfolio."""

from gui_lib.pushbutton import StandardPushButton
from gui_lib.treeview.treeview import ResizableTreeview
from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from xlrd import XLRDError

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


class PortfolioSummaryWidget(QtWidgets.QWidget):
    """Widget used to show Portfolio summary data."""

    EMPTY_SPACE = Window.DEFAULT_BORDER_SIZE

    def __init__(self, PortfolioDataFrame):
        """Create the PortfolioSummaryWidget object.

        Basically, it has a 'table' and a 'expand/collapse lines push button'.

        Arguments:
        - PortfolioDataFrame: the portfolio pandas dataframe
        """
        # Inheritance
        super().__init__()
        spacing = PortfolioSummaryWidget.EMPTY_SPACE

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

    def clearData(self):
        """Clear the treeview data lines."""
        self.__PortfolioTreeview.clearData()

    def updateData(self, dataframe):
        """Update the treeview data lines."""
        self.__PortfolioViewerManager = PortfolioViewerManager(dataframe)
        self.__initTreeviewData()


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
        self.porfolio_investment = PorfolioInvestment()
        self.porfolio_investment.setFile(File)

        try:
            if self.porfolio_investment.isValidFile():
                self.porfolio_investment.run()
                self.extrato = self.porfolio_investment.getExtrato()
                self.variable_income = self.porfolio_investment.currentPortfolio()
                self.treasuries = self.porfolio_investment.currentTesouroDireto()
            else:
                self.extrato = None
                self.variable_income = None
                self.treasuries = None
                self.__showColumnsErrorMessage()

        except XLRDError:
            self.extrato = None
            self.variable_income = None
            self.treasuries = None
            self.__showXLRDErrorMessage()

        # Portfolio Summary tab
        self.PortfolioSummaryWidget = PortfolioSummaryWidget(self.extrato)
        self.tab01 = QtWidgets.QWidget()
        self.grid_tab01 = QtWidgets.QGridLayout()
        self.grid_tab01.setContentsMargins(0, 0, 0, 0)
        self.grid_tab01.setSpacing(0)
        self.grid_tab01.addWidget(self.PortfolioSummaryWidget)
        self.tab01.setLayout(self.grid_tab01)
        self.summary_tab_index = self.addTab(self.tab01, "Extrato")

        # Variable Incomes tab
        formatter = VariableIncomesFormater(self.variable_income)
        formatted_dataframe = formatter.getFormatedPortolioDataFrame()
        self.variable_treeview = ResizableTreeviewPandas(formatted_dataframe)
        self.variable_treeview.showPandas(resize_per_contents=False)
        self.tab02 = QtWidgets.QWidget()
        self.grid_tab02 = QtWidgets.QGridLayout()
        self.grid_tab02.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid_tab02.setSpacing(spacing)
        self.grid_tab02.addWidget(self.variable_treeview)
        self.tab02.setLayout(self.grid_tab02)
        self.variable_tab_index = self.addTab(self.tab02, "Renda Variável")

        # Treasuries tab
        formatter = TreasuriesFormater(self.treasuries)
        formatted_dataframe = formatter.getFormatedPortolioDataFrame()
        self.treasuries_treeview = ResizableTreeviewPandas(formatted_dataframe)
        self.treasuries_treeview.showPandas(resize_per_contents=False)
        self.tab03 = QtWidgets.QWidget()
        self.grid_tab03 = QtWidgets.QGridLayout()
        self.grid_tab03.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid_tab03.setSpacing(spacing)
        self.grid_tab03.addWidget(self.treasuries_treeview)
        self.tab03.setLayout(self.grid_tab03)
        self.treasuries_tab_index = self.addTab(self.tab03, "Tesouro Direto")

        # Connect tab event
        self.currentChanged.connect(self.onChange)

    def __showColumnsErrorMessage(self):
        msg = "O arquivo selecionado é inválido.\n\n"
        msg += "Por favor, verifique se as seguintes colunas existem no arquivo:\n"
        for title in self.porfolio_investment.getExpectedColumnsTitleList():
            msg += "\n - " + title
        QMessageBox.warning(self, "Análise de Portfólio", msg, QMessageBox.Ok)

    def __showXLRDErrorMessage(self):
        msg = "O arquivo selecionado é inválido.\n\n"
        msg += "Por favor, verifique se o arquivo contém apenas 1 aba."
        QMessageBox.warning(self, "Análise de Portfólio", msg, QMessageBox.Ok)

    def onChange(self, index):
        """Onchange tab method to render table columns."""
        if index == self.variable_tab_index:
            self.variable_treeview.resizeColumnsToTreeViewWidth()
        elif index == self.treasuries_tab_index:
            self.treasuries_treeview.resizeColumnsToTreeViewWidth()

    def clearData(self):
        """Clear the treeview data lines."""
        self.PortfolioSummaryWidget.clearData()
        self.variable_treeview.clearData()
        self.treasuries_treeview.clearData()

    def updateData(self, file_name):
        """Update the treeview data lines."""
        self.porfolio_investment = PorfolioInvestment()
        self.porfolio_investment.setFile(file_name)

        try:
            if self.porfolio_investment.isValidFile():
                self.porfolio_investment.run()

                self.extrato = self.porfolio_investment.getExtrato()
                self.PortfolioSummaryWidget.updateData(self.extrato)

                self.variable_income = self.porfolio_investment.currentPortfolio()
                formatter = VariableIncomesFormater(self.variable_income)
                formatted_dataframe = formatter.getFormatedPortolioDataFrame()
                self.variable_treeview.setDataframe(formatted_dataframe)
                self.variable_treeview.showPandas(resize_per_contents=False)

                self.treasuries = self.porfolio_investment.currentTesouroDireto()
                formatter = TreasuriesFormater(self.treasuries)
                formatted_dataframe = formatter.getFormatedPortolioDataFrame()
                self.treasuries_treeview.setDataframe(formatted_dataframe)
                self.treasuries_treeview.showPandas(resize_per_contents=False)

            else:
                self.__showColumnsErrorMessage()

        except XLRDError:
            self.extrato = None
            self.variable_income = None
            self.treasuries = None
            self.__showXLRDErrorMessage()
