"""File to handle Opened Investment Summary for Summary tab."""

import pandas as pd
from gui_lib.treeview.format_applier import EasyFormatter
from indexer_lib.dataframe_filter import DataframeFilter


class OpenedSummaryFormatter(EasyFormatter):
    """This class is useful to format Opened Investment Summary dataFrames.

    Basically, here we manipulate the dataframe to define:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - dataframe: the portfolio pandas dataframe
    """

    def __init__(self, dataframe):
        """Create the OpenedSummaryFormatter object."""
        column_type_dict = {
            "Mercado": "s",
            "Valor_Investido": "$",
            "Valor_Acumulado": "$",
            "Acumulado-Investido": "$",
        }
        super().__init__(dataframe, column_type_dict)


class OpenedSummaryInfo:
    """Class to show data related to Opened Investments."""

    def __init__(self, extrato_df):
        """Create the OpenedSummaryInfo object."""
        from portfolio_lib.portfolio_history import OperationsHistory

        op_history = OperationsHistory(extrato_df)
        self.df_opened = op_history.getOpenedOperationsDataframe()

        # Useful lists
        self.mkt_list = self._getMarketList()
        self.mkt_df_list = self._getMarketDfList()
        self._setValueLists()

        # Main Dataframe
        self.mkt_df = pd.DataFrame()
        self.mkt_df["Mercado"] = self.mkt_list
        self.mkt_df["Valor_Investido"] = self.invested_list
        self.mkt_df["Valor_Acumulado"] = self.cumulative_list
        self.mkt_df["Acumulado-Investido"] = self.delta_list

        # Sorting dataframe 'Market'
        self.mkt_df = self.mkt_df.sort_values(by=["Mercado"])

    def _getMarketList(self):
        df_filter = DataframeFilter()
        market_list = df_filter.getListFromDataframeColumn(
            self.df_opened,
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
                self.df_opened, "Mercado", market
            )
            market_df_list.append(filtered_df)
        return market_df_list

    def _setValueLists(self):
        self.invested_list = []
        self.cumulative_list = []
        self.delta_list = []
        for df in self.mkt_df_list:
            invested_val_col = df["Preço-médio Compra"] * (
                df["Quantidade Compra"] - df["Quantidade Venda"]
            )
            invested_val = invested_val_col.sum()
            cumulative_val = df["Preço-médio Venda"].sum()
            delta_val = cumulative_val - invested_val
            self.invested_list.append(invested_val)
            self.cumulative_list.append(cumulative_val)
            self.delta_list.append(delta_val)

    def __getColumnSum(self, totaldf, column):
        totaldf[column] = [self.mkt_df[column].sum()]
        return totaldf

    """Public methods."""

    def getDataframe(self):
        """Return a multi-line dataframe with useful data.

        The following columns are present:
        - Mercado
        - Valor_Investido
        - Valor_Acumulado
        - Acumulado-Investido
        """
        return self.mkt_df.copy()

    def getFormattedDataframe(self):
        """Return a multi-line formatted dataframe with useful data.

        The following columns are present:
        - Mercado
        - Valor_Investido
        - Valor_Acumulado
        - Acumulado-Investido
        """
        mkt_formatter = OpenedSummaryFormatter(self.getDataframe())
        return mkt_formatter.getFormattedDataFrame()

    def getTotalDataframe(self):
        """Return a single-line dataframe with the sum of the useful data.

        The following columns are present:
        - Mercado
        - Valor_Investido
        - Valor_Acumulado
        - Acumulado-Investido
        """
        totaldf = pd.DataFrame()
        totaldf["Mercado"] = ["TOTAL"]
        totaldf = self.__getColumnSum(totaldf, "Valor_Investido")
        totaldf = self.__getColumnSum(totaldf, "Valor_Acumulado")
        totaldf = self.__getColumnSum(totaldf, "Acumulado-Investido")
        return totaldf.copy()

    def getTotalFormattedDataframe(self):
        """Return a single-line dataframe with the sum of the useful data.

        The following columns are present:
        - Mercado
        - Valor_Investido
        - Valor_Acumulado
        - Acumulado-Investido
        """
        mkt_formatter = OpenedSummaryFormatter(self.getTotalDataframe())
        return mkt_formatter.getFormattedDataFrame()

    def getFullFormattedDataframe(self):
        """Return a multi-line dataframe, including the total line.

        The following columns are present:
        - Mercado
        - Valor_Investido
        - Valor_Acumulado
        - Acumulado-Investido
        """
        formatted_df = self.getFormattedDataframe()
        total_dataframe = self.getTotalFormattedDataframe()
        formatted_df = pd.concat(
            [formatted_df, total_dataframe],
            ignore_index=True,
            sort=False,
        )
        return formatted_df
