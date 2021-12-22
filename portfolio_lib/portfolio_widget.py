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

from portfolio_lib.portfolio_formater import TreasuriesFormater as TFormat
from portfolio_lib.portfolio_formater import VariableIncomesFormater as VFormat
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


class OperationsHistory:
    """Class to show history data related to the ticker operations."""

    def __init__(self, extrato_df):
        """Create the operations history object."""
        # Dataframe 'Extrato'
        self.extrato_df = extrato_df
        self.df_filter = DataframeFilter()

    def _sortDataframePerData(self, filtered_df):
        filtered_df = filtered_df.sort_values(by=["Data"])
        return filtered_df

    def _getFilteredDataframePerTicker(self, ticker):
        filtered_df = self.df_filter.filterDataframePerColumn(
            self.extrato_df, "Ticker", ticker
        )
        filtered_df = self._sortDataframePerData(filtered_df)
        return filtered_df

    def _getFilteredDataframePerMarket(self, market):
        filtered_df = self.df_filter.filterDataframePerColumn(
            self.extrato_df, "Mercado", market
        )
        filtered_df = self._sortDataframePerData(filtered_df)
        return filtered_df

    def _getClosedOperationsDataframe(self, filtered_df, ticker):

        operation_ID = 1

        quantity_buy = 0
        quantity_sell = 0
        price_buy = 0
        price_sell = 0
        initial_date = None
        final_date = None
        taxes = 0
        IR = 0

        market_list = []
        operation_list = []
        ticker_list = []
        initial_date_list = []
        final_date_list = []
        days_list = []
        months_list = []
        quantity_buy_list = []
        mean_price_buy_list = []
        total_price_buy_list = []
        quantity_sell_list = []
        mean_price_sell_list = []
        total_price_sell_list = []
        taxes_list = []
        IR_list = []
        gross_result_list = []
        net_result_list = []
        rentability_list = []

        def appendResults():
            market_list.append(market)
            operation_list.append("OP" + str(operation_ID))
            ticker_list.append(ticker)
            initial_date_list.append(initial_date)
            final_date_list.append(final_date)
            range_date = final_date - initial_date
            range_days = range_date.days
            range_months = (final_date.year - initial_date.year) * 12 + (
                final_date.month - initial_date.month
            )
            days_list.append(range_days)
            months_list.append(range_months)
            quantity_buy_list.append(quantity_buy)
            mean_price_buy = price_buy / quantity_buy
            mean_price_buy_list.append(mean_price_buy)
            total_price_buy = quantity_buy * mean_price_buy
            total_price_buy_list.append(total_price_buy)
            quantity_sell_list.append(quantity_sell)
            mean_price_sell = price_sell / quantity_sell
            mean_price_sell_list.append(mean_price_sell)
            total_price_sell = quantity_sell * mean_price_sell
            total_price_sell_list.append(total_price_sell)
            taxes_list.append(taxes)
            IR_list.append(IR)
            gross_result = total_price_sell - total_price_buy
            gross_result_list.append(gross_result)
            costs = taxes + IR
            net_result = gross_result - costs
            net_result_list.append(net_result)
            try:
                rentability = net_result / (total_price_buy + costs)
            except ZeroDivisionError:
                # ZeroDivisionError means (total_price_buy + costs)=0.00
                # Then, let's replace it by 0.01
                rentability = net_result / 0.01
            rentability_list.append(rentability)

        for index, data_row in filtered_df.iterrows():

            def isBuyOperation(data_row):
                return data_row["Operação"] == "Compra"

            def isSellOperation(data_row):
                return data_row["Operação"] == "Venda"

            # Set the initial date
            if isBuyOperation(data_row) or isSellOperation(data_row):

                # First part of the operation
                if initial_date is None:
                    if data_row["Operação"] == "Compra":
                        quantity_buy += data_row["Quantidade"]
                        price_buy += data_row["Preço Total"]
                    elif data_row["Operação"] == "Venda":
                        quantity_sell += data_row["Quantidade"]
                        price_sell += data_row["Preço Total"]
                    taxes += data_row["Taxas"]
                    IR += data_row["IR"]
                    initial_date = data_row["Data"]
                    market = data_row["Mercado"]

                # Second part of the operation
                else:
                    if data_row["Operação"] == "Compra":
                        quantity_buy += data_row["Quantidade"]
                        price_buy += data_row["Preço Total"]
                    elif data_row["Operação"] == "Venda":
                        quantity_sell += data_row["Quantidade"]
                        price_sell += data_row["Preço Total"]
                    taxes += data_row["Taxas"]
                    IR += data_row["IR"]
                    if quantity_buy == quantity_sell:
                        final_date = data_row["Data"]

                # Register the data in the lists
                if (initial_date is not None) and (final_date is not None):
                    appendResults()
                    quantity_buy = 0
                    quantity_sell = 0
                    price_buy = 0
                    price_sell = 0
                    initial_date = None
                    final_date = None
                    taxes = 0
                    IR = 0
                    operation_ID += 1

        operations_df = pd.DataFrame()
        operations_df["Mercado"] = market_list
        operations_df["Ticker"] = ticker_list
        operations_df["Operação"] = operation_list
        operations_df["Data Inicial"] = initial_date_list
        operations_df["Data Final"] = final_date_list
        operations_df["Duração dias"] = days_list
        operations_df["Duração meses"] = months_list
        operations_df["Quantidade Compra"] = quantity_buy_list
        operations_df["Preço-médio Compra"] = mean_price_buy_list
        operations_df["Preço-total Compra"] = total_price_buy_list
        operations_df["Quantidade Venda"] = quantity_sell_list
        operations_df["Preço-médio Venda"] = mean_price_sell_list
        operations_df["Preço-total Venda"] = total_price_sell_list
        operations_df["Taxas"] = taxes_list
        operations_df["IR"] = IR_list
        operations_df["Venda-Compra Realizado"] = gross_result_list
        operations_df["Líquido Realizado"] = net_result_list
        operations_df["Rentabilidade Líquida"] = rentability_list
        return operations_df

    def getClosedOperationsPerTicker(self, ticker):
        """Return a dataframe of closed operations related to the ticker."""
        filtered_df = self._getFilteredDataframePerTicker(ticker)
        filtered_df = self._getClosedOperationsDataframe(filtered_df, ticker)
        return filtered_df

    def getClosedOperationsPerMarket(self, market):
        """Return a dataframe of closed operations related to the market."""
        # Filter per market
        filtered_df = self._getFilteredDataframePerMarket(market)

        # Remove duplicates
        ticker_list = self.df_filter.getListFromDataframeColumn(
            filtered_df,
            "Ticker",
        )
        ticker_list = list(set(ticker_list))

        # Run per each ticker to create an operations dataframe
        operations_mkt_df = pd.DataFrame({})
        for ticker in ticker_list:
            ticker_df = self._getFilteredDataframePerTicker(ticker)
            ticker_df = self._getClosedOperationsDataframe(ticker_df, ticker)
            operations_mkt_df = pd.concat(
                [operations_mkt_df, ticker_df],
                ignore_index=True,
                sort=False,
            )
        return operations_mkt_df

    def getClosedOperationsDataframe(self):
        """Return a dataframe of closed operations."""
        operations_mkt_df = pd.DataFrame({})
        mkt_info = MarketInformation(self.extrato_df)
        mkt_list = mkt_info._getMarketList()
        for market in mkt_list:
            df_closed_history = self.getClosedOperationsPerMarket(market)
            operations_mkt_df = pd.concat(
                [operations_mkt_df, df_closed_history],
                ignore_index=True,
                sort=False,
            )
        if mkt_list:
            operations_mkt_df = operations_mkt_df.sort_values(
                by=["Mercado", "Ticker", "Operação"]
            )
        return operations_mkt_df

    def getFormattedClosedOperationsDataframe(self):
        """Return a formatted dataframe of closed operations."""
        operations_mkt_df = self.getClosedOperationsDataframe()

        # Formatter
        op_formatter = TreeviewFormatApplier()
        op_formatter.setDataframe(operations_mkt_df)
        op_formatter.setRequiredString(
            [
                "Mercado",
                "Ticker",
                "Operação",
            ]
        )
        op_formatter.setCurrencyType(
            [
                "Preço-médio Compra",
                "Preço-total Compra",
                "Preço-médio Venda",
                "Preço-total Venda",
                "Taxas",
                "IR",
                "Venda-Compra Realizado",
                "Líquido Realizado",
            ]
        )
        op_formatter.setDateType(
            [
                "Data Inicial",
                "Data Final",
            ]
        )
        op_formatter.setFloatType(
            [
                "Duração dias",
                "Duração meses",
                "Quantidade Compra",
                "Quantidade Venda",
            ]
        )
        op_formatter.setPercentageType(
            [
                "Rentabilidade Líquida",
            ]
        )
        op_formatter.runFormatter()
        return op_formatter.getFormatedDataFrame()


class MarketInformation:
    """Class to show data related to 'market' column."""

    def __init__(self, extrato_df):
        """Create the market information object."""
        # Dataframe 'Extrato'
        self.extrato_df = extrato_df

        # Useful lists
        self.mkt_list = self._getMarketList()
        self.mkt_df_list = self._getMarketDfList()
        fee, incomeTax, dividend, jcp = self._getMarketValuesList()
        gross_result_list = self._getGrossResultList()

        # Dataframe 'Market'
        self.mkt_df = pd.DataFrame()
        self.mkt_df["Mercado"] = self.mkt_list
        self.mkt_df["Taxas"] = fee
        self.mkt_df["IR"] = incomeTax
        self.mkt_df["Dividendos"] = dividend
        self.mkt_df["JCP"] = jcp
        self.mkt_df["Venda-Compra Realizado"] = gross_result_list
        earns = (
            self.mkt_df["Dividendos"]
            + self.mkt_df["JCP"]
            + self.mkt_df["Venda-Compra Realizado"]
        )
        costs = self.mkt_df["Taxas"] + self.mkt_df["IR"]
        self.mkt_df["Líquido Realizado"] = earns - costs

        # Sorting dataframe 'Market'
        self.mkt_df = self.mkt_df.sort_values(by=["Mercado"])

        # Formatter
        self.mkt_formatter = TreeviewFormatApplier()
        self.mkt_formatter.setDataframe(self.mkt_df)
        self.mkt_formatter.setRequiredString(["Mercado"])
        self.mkt_formatter.setCurrencyType(
            [
                "Taxas",
                "IR",
                "Dividendos",
                "JCP",
                "Venda-Compra Realizado",
                "Líquido Realizado",
            ]
        )

    def _getGrossResultList(self):
        gross_result_list = []
        op_history = OperationsHistory(self.extrato_df)
        for market in self.mkt_list:
            df_closed_history = op_history.getClosedOperationsPerMarket(market)
            gross_result = df_closed_history["Venda-Compra Realizado"].sum()
            gross_result_list.append(gross_result)
        return gross_result_list

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
        for market in self.mkt_list:
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
        for df in self.mkt_df_list:
            fee, incomeTax, dividend, jcp = self._getCalculatedValues(df)
            fee_list.append(fee)
            incomeTax_list.append(incomeTax)
            dividend_list.append(dividend)
            jcp_list.append(jcp)
        return fee_list, incomeTax_list, dividend_list, jcp_list

    def getDataframe(self):
        """Return a dataframe with useful data.

        The following columns are present:
        - Mercado
        - Taxas
        - IR
        - Dividendos
        - JCP
        - Venda-Compra Realizado
        - Líquido Realizado
        """
        return self.mkt_df.copy()

    def getFormattedDataframe(self):
        """Return a formatted dataframe with useful data.

        The following columns are present:
        - Mercado
        - Taxas
        - IR
        - Dividendos
        - JCP
        - Venda-Compra Realizado
        - Líquido Realizado
        """
        self.mkt_formatter.setDataframe(self.mkt_df.copy())
        self.mkt_formatter.runFormatter()
        return self.mkt_formatter.getFormatedDataFrame().copy()

    def getTotalDataframe(self):
        """Return a dataframe with the sum of the useful data.

        The following columns are present:
        - Mercado
        - Taxas
        - IR
        - Dividendos
        - JCP
        - Venda-Compra Realizado
        - Líquido Realizado
        """
        totaldf = pd.DataFrame()
        totaldf["Mercado"] = ["TOTAL"]
        totaldf["Taxas"] = [self.mkt_df["Taxas"].sum()]
        totaldf["IR"] = [self.mkt_df["IR"].sum()]
        totaldf["Dividendos"] = [self.mkt_df["Dividendos"].sum()]
        totaldf["JCP"] = [self.mkt_df["JCP"].sum()]
        totaldf["Venda-Compra Realizado"] = [
            self.mkt_df["Venda-Compra Realizado"].sum(),
        ]
        totaldf["Líquido Realizado"] = [
            self.mkt_df["Líquido Realizado"].sum(),
        ]
        return totaldf.copy()

    def getTotalFormattedDataframe(self):
        """Return a formatted dataframe with the sum of the useful data.

        The following columns are present:
        - Mercado
        - Taxas
        - IR
        - Dividendos
        - JCP
        - Venda-Compra Realizado
        - Líquido Realizado
        """
        # Formatter
        mkt_formatter = TreeviewFormatApplier()
        mkt_formatter.setDataframe(self.getTotalDataframe())
        mkt_formatter.setRequiredString(["Mercado"])
        mkt_formatter.setCurrencyType(
            [
                "Taxas",
                "IR",
                "Dividendos",
                "JCP",
                "Venda-Compra Realizado",
                "Líquido Realizado",
            ]
        )
        mkt_formatter.runFormatter()
        return mkt_formatter.getFormatedDataFrame().copy()


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

    def addTotalLine(self, dataframe, columns_list, target_column):
        """Include a new line in the dataframe related to the total values."""
        total_df = pd.DataFrame()

        # Sum the useful columns
        for column in columns_list:
            self.__sumValueColumn(dataframe, total_df, column)

        # Make up the columns to avoid displaying unexpected N/A values
        self.__makeUpColumns(total_df, target_column, columns_list, dataframe)

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
                "Proventos",
                "Resultado liquido",
            ],
            "Mercado",
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
                "Proventos",
                "Resultado liquido",
            ],
            "Ticker",
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

    def onChangeAction(self):
        """Execute during the onChange method."""
        self.treasuries_treeview.resizeColumnsToTreeViewWidth()

    def getTabIndex(self):
        """Return the Tab index."""
        return self.TabIndex


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
        self.mkt_info = MarketInformation(dataframe)
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
        self.mkt_info = MarketInformation(dataframe)
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
                self.treasuries = self.investment.currentTesouroDireto()
                self.short_summary = self.extrato.copy()
                return True
            else:
                self.extrato = None
                self.variable_income = None
                self.treasuries = None
                self.short_summary = None
                self.__showColumnsErrorMessage()
                return False
        except XLRDError:
            self.extrato = None
            self.variable_income = None
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
            self.TreasuriesTab,
            self.ShortSummaryTab,
        ]

    def __setTabDataframeList(self):
        self.TabDataframeList = [
            self.extrato,
            self.variable_income,
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

    def setNewData(self, File):
        """Set the new treeview data lines."""
        if self.setPortfolioInvestment(File):

            self.ExtratoTab = ExtratoTabInterface(self.__addNewTab)
            self.ExtratoTab.setNewData(self.extrato)

            self.VariableTab = VariableTabInterface(self.__addNewTab)
            self.VariableTab.setNewData(self.variable_income)

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
