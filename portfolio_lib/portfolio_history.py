"""This file help us to detail the history about the Portfolio operations."""

from datetime import datetime

import pandas as pd
from gui_lib.treeview.format_applier import TreeviewFormatApplier
from indexer_lib.dataframe_filter import DataframeFilter


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


class OperationsHistory:
    """Class to show history data related to the ticker operations."""

    def __init__(self, extrato_df):
        """Create the operations history object."""
        self.extrato_df = extrato_df
        self.df_filter = DataframeFilter()

    def _sortDataframePerData(self, filtered_df):
        filtered_df = filtered_df.sort_values(by=["Data"])
        return filtered_df

    def _getFilteredDataframePerTicker(self, ticker):
        fdf = self.df_filter.filterDataframePerColumn(
            self.extrato_df,
            "Ticker",
            ticker,
        )
        fdf = self._sortDataframePerData(fdf)
        return fdf

    def _getFilteredDataframePerMarket(self, market):
        filtered_df = self.df_filter.filterDataframePerColumn(
            self.extrato_df, "Mercado", market
        )
        filtered_df = self._sortDataframePerData(filtered_df)
        return filtered_df

    def __getDefaultHistoryDataframe(self):
        col_list = [
            "Mercado",
            "Ticker",
            "Indexador",
            "Taxa Contratada",
            "Operação",
            "Data Inicial",
            "Data Final",
            "Duração dias",
            "Duração meses",
            "Quantidade Compra",
            "Preço-médio Compra",
            "Preço-total Compra",
            "Quantidade Venda",
            "Preço-médio Venda",
            "Preço-total Venda",
            "Taxas",
            "IR",
            "Dividendos",
            "JCP",
            "Venda-Compra Realizado",
            "Líquido Realizado",
            "Rentabilidade Líquida",
        ]
        return pd.DataFrame(columns=col_list)

    def _getHistOperationsDataframe(self, filtered_df, ticker, closed=True):

        operation_ID = 1

        quantity_buy = 0
        quantity_sell = 0
        price_buy = 0
        price_sell = 0
        rate_price_buy = 0
        initial_date = None
        final_date = None
        indexer = None

        market_list = []
        operation_list = []
        ticker_list = []
        indexer_list = []
        contracted_rate_list = []
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
        dividend_list = []
        JCP_list = []
        gross_result_list = []
        net_result_list = []
        rentability_list = []

        def isBuyOperation(data_row):
            return data_row["Operação"] == "Compra"

        def isSellOperation(data_row):
            return data_row["Operação"] == "Venda"

        def isInitialDateEmpty():
            return initial_date is None

        def isValidInitialDate():
            return initial_date is not None

        def isValidFinalDate():
            return final_date is not None

        def appendResults():
            market_list.append(market)
            operation_list.append("OP" + str(operation_ID))
            ticker_list.append(ticker)
            indexer_list.append(indexer)
            try:
                contracted_rate = rate_price_buy / price_buy
            except ZeroDivisionError:
                contracted_rate = ""
            contracted_rate_list.append(contracted_rate)
            initial_date_list.append(initial_date)
            final_date_list.append(final_date)
            range_date = final_date - initial_date
            range_days = range_date.days
            range_months = range_days / 30
            days_list.append(range_days)
            months_list.append(range_months)
            quantity_buy_list.append(quantity_buy)
            try:
                mean_price_buy = price_buy / quantity_buy
            except ZeroDivisionError:
                mean_price_buy = 0.0
            mean_price_buy_list.append(mean_price_buy)
            total_price_buy = quantity_buy * mean_price_buy
            total_price_buy_list.append(total_price_buy)
            quantity_sell_list.append(quantity_sell)
            try:
                mean_price_sell = price_sell / quantity_sell
            except ZeroDivisionError:
                mean_price_sell = 0.0
            mean_price_sell_list.append(mean_price_sell)
            total_price_sell = quantity_sell * mean_price_sell
            total_price_sell_list.append(total_price_sell)
            dividenddf = filtered_df.loc[
                (filtered_df["Data"] >= initial_date)
                & (filtered_df["Data"] <= final_date)
            ]
            taxes = dividenddf["Taxas"].sum()
            taxes_list.append(taxes)
            IR = dividenddf["IR"].sum()
            IR_list.append(IR)
            dividend = dividenddf["Dividendos"].sum()
            dividend_list.append(dividend)
            JCP = dividenddf["JCP"].sum()
            JCP_list.append(JCP)
            gross_result = total_price_sell - total_price_buy
            gross_result_list.append(gross_result)
            costs = taxes + IR
            earns = dividend + JCP
            net_result = gross_result - costs + earns
            net_result_list.append(net_result)
            try:
                rentability = net_result / (total_price_buy + costs)
            except ZeroDivisionError:
                # ZeroDivisionError means (total_price_buy + costs)=0.00
                # Then, let's replace it by 0.01
                rentability = net_result / 0.01
            rentability_list.append(rentability)

        lines = 0
        fdf = filtered_df[filtered_df["Operação"].isin(["Compra", "Venda"])]
        total_lines = len(fdf)
        for index, data_row in fdf.iterrows():
            lines += 1

            # Set the initial date
            if isBuyOperation(data_row) or isSellOperation(data_row):

                # First part of the operation
                if isInitialDateEmpty():
                    if data_row["Operação"] == "Compra":
                        quantity_buy += data_row["Quantidade"]
                        price_buy += data_row["Preço Total"]
                        rate = data_row["Rentabilidade Contratada"]
                        price = data_row["Preço Total"]
                        rate_price_buy += rate * price
                    elif data_row["Operação"] == "Venda":
                        quantity_sell += data_row["Quantidade"]
                        price_sell += data_row["Preço Total"]
                    indexer = data_row["Indexador"]
                    initial_date = data_row["Data"]
                    market = data_row["Mercado"]

                # Second part of the operation
                else:
                    if data_row["Operação"] == "Compra":
                        quantity_buy += data_row["Quantidade"]
                        price_buy += data_row["Preço Total"]
                        rate = data_row["Rentabilidade Contratada"]
                        price = data_row["Preço Total"]
                        rate_price_buy += rate * price
                    elif data_row["Operação"] == "Venda":
                        quantity_sell += data_row["Quantidade"]
                        price_sell += data_row["Preço Total"]
                    indexer = data_row["Indexador"]
                    if quantity_buy == quantity_sell:
                        final_date = data_row["Data"]

                # Register the data in the lists if 'closed_operation' is found
                if isValidInitialDate() and isValidFinalDate():
                    if closed:
                        appendResults()
                    quantity_buy = 0
                    quantity_sell = 0
                    price_buy = 0
                    price_sell = 0
                    rate_price_buy = 0
                    initial_date = None
                    final_date = None
                    operation_ID += 1
                    indexer = None

                # Register the data in the lists if 'opened_operation' is found
                elif total_lines == lines:
                    if isValidInitialDate():
                        if not closed:
                            final_date = datetime.today()
                            appendResults()
                        quantity_buy = 0
                        quantity_sell = 0
                        price_buy = 0
                        price_sell = 0
                        rate_price_buy = 0
                        initial_date = None
                        final_date = None
                        operation_ID += 1
                        indexer = None

        operations_df = self.__getDefaultHistoryDataframe()
        operations_df["Mercado"] = market_list
        operations_df["Ticker"] = ticker_list
        operations_df["Indexador"] = indexer_list
        operations_df["Taxa Contratada"] = contracted_rate_list
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
        operations_df["Dividendos"] = dividend_list
        operations_df["JCP"] = JCP_list
        operations_df["Venda-Compra Realizado"] = gross_result_list
        operations_df["Líquido Realizado"] = net_result_list
        operations_df["Rentabilidade Líquida"] = rentability_list
        return operations_df

    def __getHistOperationsPerTicker(self, ticker, closed=True):
        filtered_df = self._getFilteredDataframePerTicker(ticker)
        filtered_df = self._getHistOperationsDataframe(
            filtered_df,
            ticker,
            closed=closed,
        )
        return filtered_df

    def __getHistOperationsPerMarket(self, market, closed=True):
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
            ticker_df = self._getHistOperationsDataframe(
                ticker_df,
                ticker,
                closed,
            )
            operations_mkt_df = pd.concat(
                [operations_mkt_df, ticker_df],
                ignore_index=True,
                sort=False,
            )
        return operations_mkt_df

    def __getHistOperationsDataframe(self, closed=True):
        operations_mkt_df = self.__getDefaultHistoryDataframe()
        mkt_info = MarketInformation(self.extrato_df)
        mkt_list = mkt_info._getMarketList()
        for market in mkt_list:
            if closed:
                df_history = self.getClosedOperationsPerMarket(market)
            else:
                df_history = self.getOpenedOperationsPerMarket(market)
            operations_mkt_df = pd.concat(
                [operations_mkt_df, df_history],
                ignore_index=True,
                sort=False,
            )
        if mkt_list:
            operations_mkt_df = operations_mkt_df.sort_values(
                by=["Mercado", "Ticker", "Operação"]
            )
        return operations_mkt_df

    def __getFormattedHistOperationsDataframe(self, closed=True):
        if closed:
            operations_mkt_df = self.getClosedOperationsDataframe()
        else:
            operations_mkt_df = self.getOpenedOperationsDataframe()

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
        op_formatter.setNonRequiredString(
            [
                "Indexador",
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
                "Dividendos",
                "JCP",
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
                "Taxa Contratada",
            ]
        )
        op_formatter.runFormatter()
        return op_formatter.getFormatedDataFrame()

    def getClosedOperationsPerTicker(self, ticker):
        """Return a dataframe of closed operations related to the ticker."""
        return self.__getHistOperationsPerTicker(ticker, True)

    def getOpenedOperationsPerTicker(self, ticker):
        """Return a dataframe of opened operations related to the ticker."""
        return self.__getHistOperationsPerTicker(ticker, False)

    def getClosedOperationsPerMarket(self, market):
        """Return a dataframe of closed operations related to the market."""
        return self.__getHistOperationsPerMarket(market, True)

    def getOpenedOperationsPerMarket(self, market):
        """Return a dataframe of opened operations related to the market."""
        return self.__getHistOperationsPerMarket(market, False)

    def getClosedOperationsDataframe(self):
        """Return a dataframe of closed operations."""
        return self.__getHistOperationsDataframe(True)

    def getOpenedOperationsDataframe(self):
        """Return a dataframe of opened operations."""
        return self.__getHistOperationsDataframe(False)

    def getFormattedClosedOperationsDataframe(self):
        """Return a formatted dataframe of closed operations."""
        return self.__getFormattedHistOperationsDataframe(True)

    def getFormattedOpenedOperationsDataframe(self):
        """Return a formatted dataframe of opened operations."""
        return self.__getFormattedHistOperationsDataframe(False)
