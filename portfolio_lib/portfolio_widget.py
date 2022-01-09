"""This file has a set of classes to display data from Portfolio."""

import pandas as pd
from gui_lib.pushbutton import StandardPushButton
from gui_lib.treeview.format_applier import TreeviewFormatApplier
from gui_lib.treeview.treeview import ResizableTreeview
from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from indexer_lib.dataframe_filter import DataframeFilter
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from xlrd import XLRDError

from portfolio_lib.portfolio_formater import FixedIncomesFormater as FixFormat
from portfolio_lib.portfolio_formater import TreasuriesFormater as TFormat
from portfolio_lib.portfolio_formater import VariableIncomesFormater as VFormat
from portfolio_lib.portfolio_history import MarketInformation as MktInfo
from portfolio_lib.portfolio_history import OperationsHistory as OpInfo
from portfolio_lib.portfolio_investment import PortfolioInvestment
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


class TabViewerWidget:
    """Widget used to show tabs related to PortfolioViewerWidget."""

    def __init__(self, special_widget_list, tab_title, spacing=0):
        """Create the TabViewerWidget object.

        The 'special_widget_list' argument is a list of any widgets
        based on the 'QtWidgets.QWidget' class.

        The 'tab_title' is the text on the tab.
        """
        self.tab_title = tab_title
        self.tab = QtWidgets.QWidget()
        self.grid_tab = QtWidgets.QGridLayout()
        self.grid_tab.setContentsMargins(
            spacing,
            spacing,
            spacing,
            spacing,
        )
        self.grid_tab.setSpacing(spacing)
        for special_widget in special_widget_list:
            self.grid_tab.addWidget(special_widget)
        self.tab.setLayout(self.grid_tab)

    def getTab(self):
        """Return the 'Tab' object."""
        return self.tab

    def getGridTab(self):
        """Return the 'GridTab' object."""
        return self.grid_tab

    def getTabTitle(self):
        """Return the 'Tab' title."""
        return self.tab_title

    def setTabIndex(self, tab_index):
        """Set the tab index."""
        self.tab_index = tab_index

    def getTabIndex(self):
        """Return the tab index."""
        return self.tab_index


class TabViewerInterface:
    """Tab Interface to work together with PortfolioViewerWidget."""

    def __init__(self):
        """Create the TabViewerInterface object."""
        pass

    def __sumValueColumn(self, dataframe, total_df, column_title):
        total_df[column_title] = [dataframe[column_title].sum()]

    def __sumPercentageColumn(self, total_df, percentage, initial, final):
        initial_value = total_df[initial].sum()
        final_value = total_df[final].sum()
        total_df[percentage] = [final_value / initial_value]

    def __makeUpColumns(self, total_df, target_column, columns_list, df):
        # Include the 'TOTAL' cell
        total_df[target_column] = ["TOTAL"]

        # All the column titles from the original dataframe
        all_df_columns_set = set(list(df))

        # All the columns with total values addded
        avoid_list = columns_list.copy()
        avoid_list.extend([target_column])

        # Fill with empty space ' ' the other columns
        target_empty_columns = all_df_columns_set.difference(avoid_list)
        for column in target_empty_columns:
            total_df[column] = ["-"]

    def addTotalLine(
        self,
        dataframe,
        columns_list,
        target_column,
        perc_lists=None,
    ):
        """Include a new line in the dataframe with the total values.

        Arguments:
        - dataframe: the dataframe with multiple columns
        - columns_list: the columns with 'simple sum' values
        - target_column: the column where the 'TOTAL' text will be inserted
        - perc_lists: a list of lists where:
          * 1st item: the percentage column title
          * 2nd item: the initial value column title
          * 3rd item: the final value column title
        """
        total_df = pd.DataFrame()

        # Sum the useful columns
        for column in columns_list:
            self.__sumValueColumn(dataframe, total_df, column)

        # Include the percentage columns
        if perc_lists:
            for perc in perc_lists:
                percentage_column = perc[0]
                initial_column = perc[1]
                final_column = perc[2]
                self.__sumPercentageColumn(
                    total_df,
                    percentage_column,
                    initial_column,
                    final_column,
                )

        # Make up the columns to avoid displaying unexpected N/A values
        avoid_list = []
        if perc_lists:
            for perc_list in perc_lists:
                avoid_list.extend(perc_list)
        avoid_list.extend(columns_list)
        avoid_list.extend([target_column])
        self.__makeUpColumns(total_df, target_column, avoid_list, dataframe)

        # Concatenate the dataframes
        dataframe = pd.concat(
            [dataframe, total_df],
            ignore_index=True,
            sort=False,
        )

        return dataframe

    def setNewData(self):
        """Abstract method to set new data."""
        pass

    def clearData(self):
        """Abstract method to clear data."""
        pass

    def updateData(self):
        """Abstract method to update data."""
        pass

    def onChangeAction(self):
        """Abstract method to execute onChange method."""
        pass

    def getTabIndex(self):
        """Abstract method to return the Tab index."""
        pass


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
                "Preço mercado-pago",
                "Proventos",
                "Custos",
                "Resultado liquido",
            ],
            "Mercado",
            [
                [
                    "Rentabilidade mercado-pago",
                    "Preço pago",
                    "Preço mercado-pago",
                ],
                [
                    "Rentabilidade liquida",
                    "Preço pago",
                    "Resultado liquido",
                ],
            ],
        )
        return dataframe

    def setNewData(self, dataframe):
        """Set the data table."""
        dataframe = self.__addTotalLine(dataframe)
        self.formatter = VFormat(dataframe)
        formatted_df = self.formatter.getFormatedPortolioDataFrame()
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
        self.formatter = VFormat(dataframe)
        formatted_dataframe = self.formatter.getFormatedPortolioDataFrame()
        self.variable_treeview.clearData()
        self.variable_treeview.setDataframe(formatted_dataframe)
        self.variable_treeview.showPandas(resize_per_contents=False)
        self.onChangeAction()

    def onChangeAction(self):
        """Execute during the onChange method."""
        self.variable_treeview.resizeColumnsToTreeViewWidth()

    def getTabIndex(self):
        """Return the Tab index."""
        return self.TabIndex


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
                "Preço mercado-pago",
                "Proventos",
                "Custos",
                "Resultado liquido",
            ],
            "Ticker",
            [
                [
                    "Rentabilidade mercado-pago",
                    "Preço pago",
                    "Preço mercado-pago",
                ],
                [
                    "Rentabilidade liquida",
                    "Preço pago",
                    "Resultado liquido",
                ],
            ],
        )
        return dataframe

    def setNewData(self, dataframe):
        """Set the data table."""
        dataframe = self.__addTotalLine(dataframe)
        self.formatter = TFormat(dataframe)
        formatted_df = self.formatter.getFormatedPortolioDataFrame()
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
        self.formatter = TFormat(dataframe)
        formatted_df = self.formatter.getFormatedPortolioDataFrame()
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


class FixedIncomeTabInterface(TabViewerInterface):
    """FixedIncomeTabInterface to work together with PortfolioViewerWidget."""

    def __init__(self, addNewTabMethod):
        """Create the FixedIncomeTabInterface object."""
        super().__init__()
        self.addNewTabMethod = addNewTabMethod
        self.formatter = None
        self.treeview = None
        self.tab = None

    def __addTotalLine(self, dataframe):
        dataframe = self.addTotalLine(
            dataframe,
            [
                "Preço pago",
                "Preço mercado",
                "Preço mercado-pago",
                "Proventos",
                "Custos",
                "Resultado liquido",
            ],
            "Ticker",
            [
                [
                    "Rentabilidade mercado-pago",
                    "Preço pago",
                    "Preço mercado-pago",
                ],
                [
                    "Rentabilidade liquida",
                    "Preço pago",
                    "Resultado liquido",
                ],
            ],
        )
        return dataframe

    def setNewData(self, dataframe):
        """Set the data table."""
        dataframe = self.__addTotalLine(dataframe)
        self.formatter = FixFormat(dataframe)
        formatted_df = self.formatter.getFormatedPortolioDataFrame()
        self.treeview = ResizableTreeviewPandas(formatted_df)
        self.treeview.showPandas(resize_per_contents=False)
        self.tab = TabViewerWidget(
            [self.treeview],
            "Renda Fixa",
            spacing=Window.DEFAULT_BORDER_SIZE,
        )
        self.tab_index = self.addNewTabMethod(self.tab)
        self.onChangeAction()

    def clearData(self):
        """Clear the data table."""
        self.treeview.clearData()

    def updateData(self, dataframe):
        """Update the data table."""
        dataframe = self.__addTotalLine(dataframe)
        self.formatter = FixFormat(dataframe)
        formatted_df = self.formatter.getFormatedPortolioDataFrame()
        self.treeview.clearData()
        self.treeview.setDataframe(formatted_df)
        self.treeview.showPandas(resize_per_contents=False)
        self.onChangeAction()

    def onChangeAction(self):
        """Execute during the onChange method."""
        self.treeview.resizeColumnsToContents()

    def getTabIndex(self):
        """Return the Tab index."""
        return self.tab_index


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
        self.mkt_info = MktInfo(dataframe)
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
        self.operations_info = OpInfo(dataframe)
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
        self.mkt_info = MktInfo(dataframe)
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
        self.operations_info = OpInfo(dataframe)
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


class PortfolioViewerWidget(QtWidgets.QTabWidget):
    """Widget used to show data related to Portfolio."""

    def __init__(self, File):
        """Create the PortfolioViewerWidget object.

        Arguments:
        - File: the Portfolio file
        """
        super().__init__()
        self.setNewData(File)

        # Connect tab event
        self.currentChanged.connect(self.onChange)

    def __updateMainDataframes(self):
        try:
            if self.investment.isValidFile():
                self.investment.run()
                self.extrato = self.investment.getExtrato()
                self.variable_income = self.investment.currentPortfolio()
                self.fixed_income = self.investment.currentRendaFixa()
                self.treasuries = self.investment.currentTesouroDireto()
                self.short_summary = self.extrato.copy()
                return True
            else:
                self.extrato = None
                self.variable_income = None
                self.fixed_income = None
                self.treasuries = None
                self.short_summary = None
                self.__showColumnsErrorMessage()
                return False
        except XLRDError:
            self.extrato = None
            self.variable_income = None
            self.fixed_income = None
            self.treasuries = None
            self.short_summary = None
            self.__showXLRDErrorMessage()
            return False

    def __addNewTab(self, tab_widget):
        tab_index = self.addTab(
            tab_widget.getTab(),
            tab_widget.getTabTitle(),
        )
        tab_widget.setTabIndex(tab_index)
        return tab_index

    def __showColumnsErrorMessage(self):
        msg = "O arquivo selecionado é inválido.\n\n"
        msg += "Por favor, verifique se as colunas existem no arquivo:\n"
        for title in self.investment.getExpectedColumnsTitleList():
            msg += "\n - " + title
        QMessageBox.warning(self, "Análise de Portfólio", msg, QMessageBox.Ok)

    def __showXLRDErrorMessage(self):
        msg = "O arquivo selecionado é inválido.\n\n"
        msg += "Por favor, verifique se o arquivo contém apenas 1 aba."
        QMessageBox.warning(self, "Análise de Portfólio", msg, QMessageBox.Ok)

    def __setTabInterfaceList(self):
        self.TabInterfaceList = [
            self.ExtratoTab,
            self.VariableTab,
            self.FixedTab,
            self.TreasuriesTab,
            self.ShortSummaryTab,
        ]

    def __setTabDataframeList(self):
        self.TabDataframeList = [
            self.extrato,
            self.variable_income,
            self.fixed_income,
            self.treasuries,
            self.short_summary,
        ]

    def setPortfolioInvestment(self, File):
        """Read the excel file and update the main dataframes."""
        self.investment = PortfolioInvestment()
        self.investment.setFile(File)
        df_updated_flag = self.__updateMainDataframes()
        self.__setTabDataframeList()
        return df_updated_flag

    def exportGoogleDriveSheet(self):
        """Export the Google Drive spreasheet."""
        self.investment.currentPortfolioGoogleDrive()

    def setNewData(self, File):
        """Set the new treeview data lines."""
        if self.setPortfolioInvestment(File):

            self.ExtratoTab = ExtratoTabInterface(self.__addNewTab)
            self.ExtratoTab.setNewData(self.extrato)

            self.VariableTab = VariableTabInterface(self.__addNewTab)
            self.VariableTab.setNewData(self.variable_income)

            self.FixedTab = FixedIncomeTabInterface(self.__addNewTab)
            self.FixedTab.setNewData(self.fixed_income)

            self.TreasuriesTab = TreasuriesTabInterface(self.__addNewTab)
            self.TreasuriesTab.setNewData(self.treasuries)

            self.ShortSummaryTab = ShortSummaryTabInterface(self.__addNewTab)
            self.ShortSummaryTab.setNewData(self.short_summary)

            self.__setTabInterfaceList()

    def clearData(self):
        """Clear the treeview data lines."""
        for tab_interface in self.TabInterfaceList:
            tab_interface.clearData()

    def updateData(self, File):
        """Update the treeview data lines."""
        if self.setPortfolioInvestment(File):
            for index in range(len(self.TabInterfaceList)):
                tab_interface = self.TabInterfaceList[index]
                tab_dataframe = self.TabDataframeList[index]
                tab_interface.updateData(tab_dataframe)

    def onChange(self, index):
        """Onchange tab method to render the table columns."""
        for tab_interface in self.TabInterfaceList:
            if index == tab_interface.getTabIndex():
                tab_interface.onChangeAction()
