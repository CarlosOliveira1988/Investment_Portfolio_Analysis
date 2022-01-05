"""This file help us to detail the history about the Portfolio operations."""

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
            range_months = range_days / 30
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
