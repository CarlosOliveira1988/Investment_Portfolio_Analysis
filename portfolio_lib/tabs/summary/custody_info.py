"""File to handle Custody Information for Summary tab."""

import pandas as pd
from gui_lib.treeview.format_applier import EasyFormatter
from indexer_lib.dataframe_filter import DataframeFilter


class CustodyFormatter(EasyFormatter):
    """This class is useful to format Custody dataFrames.

    Basically, here we manipulate the dataframe to define:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - dataframe: the portfolio pandas dataframe
    """

    def __init__(self, dataframe):
        """Create the CustodyFormatter object."""
        column_type_dict = {
            "Mercado": "s",
            "Transferência": "$",
            "Resgate": "$",
            "Taxas": "$",
            "IR": "$",
        }
        super().__init__(dataframe, column_type_dict)


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
        self.cust_df["Transferência"] = [self.deposit]
        self.cust_df["Resgate"] = [self.rescue]

    def getDataframe(self):
        """Return a multi-line dataframe with useful data.

        The following columns are present:
        - Mercado
        - Transferência
        - Resgate
        - Taxas
        - IR
        """
        return self.cust_df.copy()

    def getFormattedDataframe(self):
        """Return a multi-line formatted dataframe with useful data.

        The following columns are present:
        - Mercado
        - Transferência
        - Resgate
        - Taxas
        - IR
        """
        cust_formatter = CustodyFormatter(self.getDataframe())
        return cust_formatter.getFormattedDataFrame()
