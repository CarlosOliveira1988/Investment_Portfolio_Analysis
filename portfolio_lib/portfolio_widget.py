"""This file has a set of classes to display data from Portfolio."""

import pandas as pd
from gui_lib.pushbutton import StandardPushButton
from gui_lib.treeview.treeview import ResizableTreeview
from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from indexer_lib.dataframe_filter import DataframeFilter
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


class MarketInformation:
    def __init__(self, extrato_df):
        # Dataframe 'Extrato'
        self.extrato_df = extrato_df

        # Useful lists
        self.market_list = self._getMarketList()
        self.market_df_list = self._getMarketDfList()
        fee, incomeTax, dividend, jcp = self._getMarketValuesList()

        # Dataframe 'Market'
        self.market_df = pd.DataFrame()
        self.market_df["Mercado"] = self.market_list
        self.market_df["Taxas"] = fee
        self.market_df["IR"] = incomeTax
        self.market_df["Dividendos"] = dividend
        self.market_df["JCP"] = jcp

    def _getMarketList(self):
        df_filter = DataframeFilter()
        market_list = df_filter.getListFromDataframeColumn(
            self.extrato_df,
            "Mercado",
        )
        market_list = list(set(market_list))
        try:
            market_list.remove("Custodia")
        except ValueError:
            pass
        return market_list

    def _getMarketDfList(self):
        market_df_list = []
        for market in self.market_list:
            df_filter = DataframeFilter()
            filtered_df = df_filter.filterDataframePerColumn(
                self.extrato_df, "Mercado", market
            )
            market_df_list.append(filtered_df)
        return market_df_list

    def _getCalculatedValues(self, filtered_df):
        fee = filtered_df["Taxas"].sum()
        incomeTax = filtered_df["IR"].sum()
        dividend = filtered_df["Dividendos"].sum()
        jcp = filtered_df["JCP"].sum()
        return fee, incomeTax, dividend, jcp

    def _getMarketValuesList(self):
        fee_list = []
        incomeTax_list = []
        dividend_list = []
        jcp_list = []
        for df in self.market_df_list:
            fee, incomeTax, dividend, jcp = self._getCalculatedValues(df)
            fee_list.append(fee)
            incomeTax_list.append(incomeTax)
            dividend_list.append(dividend)
            jcp_list.append(jcp)
        return fee_list, incomeTax_list, dividend_list, jcp_list

    def getDataframe(self):
        return self.market_df


class CustodyInformation:
    def __init__(self, extrato_df):
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
        self.custody_df = pd.DataFrame()
        self.custody_df["Mercado"] = ["Custodia"]
        self.custody_df["Taxas"] = [self.fee]
        self.custody_df["IR"] = [self.incomeTax]
        self.custody_df["Dividendos"] = [self.dividend]
        self.custody_df["JCP"] = [self.jcp]
        self.custody_df["Transferência"] = [self.deposit]
        self.custody_df["Resgate"] = [self.rescue]

    def getDataframe(self):
        return self.custody_df


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

        # Short Summary tab
        extrato_df = self.extrato.copy()
        self.market_info = MarketInformation(extrato_df)
        self.market_summary_treeview = ResizableTreeviewPandas(
            self.market_info.getDataframe()
        )
        self.market_summary_treeview.showPandas(resize_per_contents=False)
        self.custody_info = CustodyInformation(extrato_df)
        self.custody_summary_treeview = ResizableTreeviewPandas(
            self.custody_info.getDataframe()
        )
        self.custody_summary_treeview.showPandas(resize_per_contents=False)
        self.tab04 = QtWidgets.QWidget()
        self.grid_tab04 = QtWidgets.QGridLayout()
        self.grid_tab04.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid_tab04.setSpacing(spacing)
        self.grid_tab04.addWidget(self.market_summary_treeview)
        self.grid_tab04.addWidget(self.custody_summary_treeview)
        self.tab04.setLayout(self.grid_tab04)
        self.short_summary_tab_index = self.addTab(self.tab04, "Resumo Extrato")

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
        elif index == self.short_summary_tab_index:
            self.custody_summary_treeview.resizeColumnsToTreeViewWidth()
            self.market_summary_treeview.resizeColumnsToTreeViewWidth()

    def clearData(self):
        """Clear the treeview data lines."""
        self.PortfolioSummaryWidget.clearData()
        self.variable_treeview.clearData()
        self.treasuries_treeview.clearData()
        self.custody_summary_treeview.clearData()
        self.market_summary_treeview.clearData()

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

                self.market_info = MarketInformation(self.extrato.copy())
                formatted_dataframe = self.market_info.getDataframe()
                self.market_summary_treeview.setDataframe(formatted_dataframe)
                self.market_summary_treeview.showPandas(resize_per_contents=False)

                self.custody_info = CustodyInformation(self.extrato.copy())
                formatted_dataframe = self.custody_info.getDataframe()
                self.custody_summary_treeview.setDataframe(formatted_dataframe)
                self.custody_summary_treeview.showPandas(resize_per_contents=False)

            else:
                self.__showColumnsErrorMessage()

        except XLRDError:
            self.extrato = None
            self.variable_income = None
            self.treasuries = None
            self.__showXLRDErrorMessage()
