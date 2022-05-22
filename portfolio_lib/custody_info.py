"""File to handle Custody Information for Summary tab."""

import pandas as pd
from gui_lib.treeview.format_applier import TreeviewFormatApplier
from indexer_lib.dataframe_filter import DataframeFilter


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
