"""File to handle Market Information for Summary tab."""

import pandas as pd
from gui_lib.treeview.format_applier import EasyFormatter
from indexer_lib.dataframe_filter import DataframeFilter


class MarketFormatter(EasyFormatter):
    """This class is useful to format Market dataFrames.

    Basically, here we manipulate the dataframe to define:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - dataframe: the portfolio pandas dataframe
    """

    def __init__(self, dataframe):
        """Create the MarketFormatter object."""
        column_type_dict = {
            "Mercado": "s",
            "Taxas": "$",
            "IR": "$",
            "Dividendos": "$",
            "JCP": "$",
            "Venda-Compra Realizado": "$",
            "Líquido Realizado": "$",
        }
        super().__init__(dataframe, column_type_dict)


class MarketInfo:
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

    """Private methods."""

    def __getColumnSum(self, totaldf, column):
        totaldf[column] = [self.mkt_df[column].sum()]
        return totaldf

    """Protected methods."""

    def _getGrossResultList(self):
        from portfolio_lib.portfolio_history import OperationsHistory

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

    """Public methods."""

    def getDataframe(self):
        """Return a multi-line dataframe with useful data.

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
        """Return a multi-line formatted dataframe with useful data.

        The following columns are present:
        - Mercado
        - Taxas
        - IR
        - Dividendos
        - JCP
        - Venda-Compra Realizado
        - Líquido Realizado
        """
        mkt_formatter = MarketFormatter(self.getDataframe())
        return mkt_formatter.getFormattedDataFrame()

    def getTotalDataframe(self):
        """Return a single-line dataframe with the sum of the useful data.

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
        totaldf = self.__getColumnSum(totaldf, "Taxas")
        totaldf = self.__getColumnSum(totaldf, "IR")
        totaldf = self.__getColumnSum(totaldf, "Dividendos")
        totaldf = self.__getColumnSum(totaldf, "JCP")
        totaldf = self.__getColumnSum(totaldf, "Venda-Compra Realizado")
        totaldf = self.__getColumnSum(totaldf, "Líquido Realizado")
        return totaldf.copy()

    def getTotalFormattedDataframe(self):
        """Return a single-line dataframe with the sum of the useful data.

        The following columns are present:
        - Mercado
        - Taxas
        - IR
        - Dividendos
        - JCP
        - Venda-Compra Realizado
        - Líquido Realizado
        """
        mkt_formatter = MarketFormatter(self.getTotalDataframe())
        return mkt_formatter.getFormattedDataFrame()

    def getFullFormattedDataframe(self):
        """Return a multi-line dataframe, including the total line.

        The following columns are present:
        - Mercado
        - Taxas
        - IR
        - Dividendos
        - JCP
        - Venda-Compra Realizado
        - Líquido Realizado
        """
        formatted_df = self.getFormattedDataframe()
        total_dataframe = self.getTotalFormattedDataframe()
        formatted_df = pd.concat(
            [formatted_df, total_dataframe],
            ignore_index=True,
            sort=False,
        )
        return formatted_df
