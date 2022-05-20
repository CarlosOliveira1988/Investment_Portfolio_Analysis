"""This file has a set of methods related to Fixed Income assets."""

from indexer_lib.fixed_income import FixedIncomeCalculation

from portfolio_lib.portfolio_assets import PortfolioAssets


class FixedIncomeAssets(PortfolioAssets):
    """Class used to manipulate the Fixed Income assets."""

    def __init__(self):
        """Create the FixedIncomeAssets object."""
        super().__init__()
        self.fixedIncomeCalc = FixedIncomeCalculation()

    """Private methods."""

    def __currentRendaFixa(self):
        # Prepare the default wallet dataframe
        market_list = ["Renda Fixa"]
        # self.setOpenedOperations(self.openedOperations)
        wallet = self.createWalletDefaultColumns(market_list)

        # Insert the current market values
        for index, row in wallet.iterrows():
            initial_date = row["Data Inicial"]
            final_date = row["Data Final"]
            indexer = row["Indexador"]
            rate = row["Taxa-média Contratada"]
            buy_price = row["Preço médio"]
            wallet.at[index, "Cotação"] = self.currentValRendaFixa(
                initial_date, final_date, indexer, rate, buy_price
            )
            wallet.at[index, "Taxa-média Ajustada"] = self.getAdjustedYield(
                rate, indexer
            )

        # Calculate values related to the wallet default columns
        self.calculateWalletDefaultColumns(market_list)

        return wallet

    """Protected methods."""

    def _checkIndexerType(self, indexer):
        self._checkStringType(indexer)
        if indexer not in ["PREFIXADO", "IPCA", "CDI"]:
            raise ValueError(
                "The indexer argument should be 'PREFIXADO', 'IPCA' or 'CDI'.",
            )

    """Public methods."""

    def currentValRendaFixa(
        self,
        initial_date,
        final_date,
        indexer,
        rate,
        buyPrice,
    ):
        """Return the current price of the related 'Renda Fixa' ticker.

        The available indexer types are:
        - PREFIXADO: the result is based in an "annual rate"
        - IPCA: the result is based in an "annual rate" + IPCA
        - CDI: the result is based in an "annual rate" * CDI
        """
        self._checkDateType(initial_date)
        self._checkDateType(final_date)
        self._checkIndexerType(indexer)
        self._checkNumberType(rate)
        self._checkNumberType(buyPrice)
        if indexer == "PREFIXADO":
            return self.fixedIncomeCalc.getValueByPrefixedRate(
                initial_date,
                final_date,
                rate,
                buyPrice,
            )
        elif indexer == "IPCA":
            return self.fixedIncomeCalc.getValueByPrefixedRatePlusIPCA(
                initial_date,
                final_date,
                rate,
                buyPrice,
            )
        elif indexer == "CDI":
            return self.fixedIncomeCalc.getValueByProportionalCDI(
                initial_date,
                final_date,
                rate,
                buyPrice,
            )
        else:
            return float(buyPrice)

    def currentRendaFixa(self):
        """Create a dataframe with all opened operations of Renda Fixa."""
        self.wallet = self.__currentRendaFixa()
        return self.wallet.copy()
