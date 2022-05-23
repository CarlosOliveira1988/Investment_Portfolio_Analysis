"""This file has a class to manage Portfolio assets."""

from datetime import datetime

import pandas as pd
from indexer_lib.months_indexers import TwelveMonthsIndexer

from portfolio_lib.portfolio_history import OperationsHistory


class PortfolioAssets:
    """Class used to manipulate the different portfolio assets."""

    def __init__(self):
        """Create the PortfolioAssets object."""
        self.wallet = self._getAssetsDefaultDataframe()
        self.openedOperations = self._getAssetsDefaultDataframe()
        self.indexers = TwelveMonthsIndexer()
        self.history = None

    """Private methods."""

    def _getAssetsDefaultDataframe(self):
        col_list = [
            "Ticker",
            "Mercado",
            "Indexador",
            "Taxa-média Contratada",
            "Taxa-média Ajustada",
            "Data Inicial",
            "Data Final",
            "Quantidade",
            "Quantidade compra",
            "Preço médio",
            "Preço médio+taxas",
            "Preço pago",
            "Compras totais",
            "Vendas parciais",
            "Proventos",
            "Custos",
            "Taxas Adicionais",
            "IR",
            "Dividendos",
            "JCP",
            "Cotação",
            "Preço mercado",
            "Mercado-pago",
            "Mercado-pago(%)",
            "Líquido parcial",
            "Líquido parcial(%)",
            "Porcentagem carteira",
        ]
        return pd.DataFrame(columns=col_list)

    def _getDefaultDataframe(self):
        return self._getAssetsDefaultDataframe()

    def __getMarketValueSum(self, market):
        df = self.wallet[self.wallet["Mercado"] == market]
        return df["Preço mercado"].sum()

    def __setTickerPercentage(self, market):
        marketValue = self.__getMarketValueSum(market)
        marketDF = self.wallet[self.wallet["Mercado"].isin([market])]
        for index, row in marketDF.iterrows():
            marketPrice = row["Preço mercado"]
            percentage = marketPrice / marketValue
            self.wallet.at[index, "Porcentagem carteira"] = percentage

    def __getTicker(self):
        return self.openedOperations["Ticker"]

    def __getMercado(self):
        return self.openedOperations["Mercado"]

    def __getIndexador(self):
        return self.openedOperations["Indexador"]

    def __getQuantidade(self):
        df = self.openedOperations
        return df["Quantidade Compra"] - df["Quantidade Venda"]

    def __getTaxa(self):
        return self.openedOperations["Taxa-média Contratada"]

    def __getTaxaAjustada(self):
        return self.openedOperations["Taxa-média Contratada"]

    def __getDataInicial(self):
        return self.openedOperations["Data Inicial"]

    def __getDataFinal(self):
        return self.openedOperations["Data Final"]

    def __getProventos(self):
        df = self.openedOperations
        return df["Dividendos"] + df["JCP"]

    def __getCustos(self):
        df = self.openedOperations
        return df["Taxas"] + df["IR"]

    def __getTaxasAdicionais(self):
        df = self.openedOperations
        return df["Taxas Venda"] + df["Outras Taxas"]

    def __getIR(self):
        return self.openedOperations["IR"]

    def __getDividendos(self):
        return self.openedOperations["Dividendos"]

    def __getJCP(self):
        return self.openedOperations["JCP"]

    def __getQuantidadeCompra(self):
        return self.openedOperations["Quantidade Compra"]

    def __getPrecoMedio(self):
        df = self.openedOperations
        priceBuy = df["Preço-médio Compra"]
        qtdBuy = df["Quantidade Compra"]
        total_price = qtdBuy * priceBuy
        total_qtd = qtdBuy
        return total_price / total_qtd

    def __getPrecoMedioTaxas(self):
        df = self.openedOperations
        mean_fee = df["Taxas Compra"] / df["Quantidade Compra"]
        return mean_fee + self.wallet["Preço médio"]

    def __getPrecoPago(self):
        return self.wallet["Quantidade"] * self.wallet["Preço médio+taxas"]

    def __getComprasTotais(self):
        columnA = "Preço médio+taxas"
        columnB = "Quantidade compra"
        return self.wallet[columnA] * self.wallet[columnB]

    def __getVendasParciais(self):
        df = self.openedOperations
        return df["Preço-médio Venda"] * df["Quantidade Venda"]

    def __getPrecoMercado(self):
        return self.wallet["Quantidade"] * self.wallet["Cotação"]

    def __getMercadoMenosPago(self):
        return self.wallet["Preço mercado"] - self.wallet["Preço pago"]

    def __getPrecoTotal(self):
        return self.wallet["Preço mercado"] + self.wallet["Vendas parciais"]

    def __getCustosAdicionais(self):
        return self.wallet["IR"] + self.wallet["Taxas Adicionais"]

    def __getPrecoAjustado(self):
        totalPrice = self.__getPrecoTotal()
        additionalCosts = self.__getCustosAdicionais()
        return totalPrice + self.wallet["Proventos"] - additionalCosts

    """Protected methods."""

    def _checkDateType(self, date):
        if not isinstance(date, datetime):
            raise TypeError(
                "The date argument should be a datetime type.",
            )

    def _checkNumberType(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError(
                "The value argument should be int/float type.",
            )

    def _checkStringType(self, value):
        if not isinstance(value, str):
            raise TypeError(
                "The value argument should be a string type.",
            )

    def _checkListType(self, value_list):
        if not isinstance(value_list, list):
            raise TypeError(
                "The value_list argument should be a list type.",
            )

    def _checkStringListType(self, value_list):
        self._checkListType(value_list)
        if value_list:
            [self._checkStringType(value) for value in value_list]
        else:
            raise ValueError(
                "The value_list argument should not be empty.",
            )

    """Public methods."""

    def getAdjustedYield(self, yield_val, adjust_type):
        """Return the 'adjusted_yield' value given an 'adjust_type'.

        The availabe 'adjust_type' are:
        - IPCA : return 'yield_val + IPCA'
        - SELIC: return 'yield_val + SELIC'
        - CDI  : return 'yield_val * CDI'
        - PREFIXADO: return 'yield_val'
        """
        if adjust_type == "IPCA":
            return yield_val + self.indexers.getIPCA()
        elif adjust_type == "SELIC":
            return yield_val + self.indexers.getSELIC()
        elif adjust_type == "CDI":
            return yield_val * self.indexers.getCDI()
        elif adjust_type == "PREFIXADO":
            return yield_val
        else:
            return 0.0

    def getColumnsTitleList(self):
        """Return a list of expected column titles."""
        return list(self.wallet)

    def setOpenedOperations(self, openedOperations):
        """Set the opened operations."""
        self.openedOperations = openedOperations.copy()

    def setExtratoDataframe(self, operations):
        """Set the operations dataframe."""
        self.history = OperationsHistory(operations)
        self.setOpenedOperations(self.history.getOpenedOperationsDataframe())

    def createWalletDefaultColumns(self, market_list):
        """Return a default dataframe with 'Wallet' columns."""
        # 'Extrato' dataframe has title and data lines
        if len(self.openedOperations):

            # Prepare the useful dataframe
            df = self.openedOperations["Mercado"].isin(market_list)
            self.openedOperations = self.openedOperations[df]
            self.openedOperations.drop_duplicates(
                subset="Ticker",
                keep="first",
                inplace=True,
            )

            # Copy the useful data to the 'wallet'
            self.wallet = self._getAssetsDefaultDataframe()
            self.wallet["Ticker"] = self.__getTicker()
            self.wallet["Mercado"] = self.__getMercado()
            self.wallet["Indexador"] = self.__getIndexador()
            self.wallet["Taxa-média Contratada"] = self.__getTaxa()
            self.wallet["Taxa-média Ajustada"] = self.__getTaxaAjustada()
            self.wallet["Data Inicial"] = self.__getDataInicial()
            self.wallet["Data Final"] = self.__getDataFinal()
            self.wallet["Proventos"] = self.__getProventos()
            self.wallet["Custos"] = self.__getCustos()
            self.wallet["Taxas Adicionais"] = self.__getTaxasAdicionais()
            self.wallet["IR"] = self.__getIR()
            self.wallet["Dividendos"] = self.__getDividendos()
            self.wallet["JCP"] = self.__getJCP()
            self.wallet["Quantidade compra"] = self.__getQuantidadeCompra()
            self.wallet["Quantidade"] = self.__getQuantidade()
            self.wallet["Preço médio"] = self.__getPrecoMedio()
            self.wallet["Preço médio+taxas"] = self.__getPrecoMedioTaxas()
            self.wallet["Preço pago"] = self.__getPrecoPago()
            self.wallet["Compras totais"] = self.__getComprasTotais()
            self.wallet["Vendas parciais"] = self.__getVendasParciais()

            # Sort the data by market and ticker
            self.wallet = self.wallet.sort_values(by=["Mercado", "Ticker"])

            return self.wallet

        # 'Extrato' dataframe has ONLY the title line
        else:
            return self._getAssetsDefaultDataframe().copy()

    def calculateWalletDefaultColumns(self, market_list):
        """Calculate default column values."""
        self.wallet["Preço mercado"] = self.__getPrecoMercado()
        deltaPrice = self.__getMercadoMenosPago()
        self.wallet["Mercado-pago"] = deltaPrice
        buyPrice = self.wallet["Preço pago"]
        self.wallet["Mercado-pago(%)"] = deltaPrice / buyPrice
        totalPriceAdjusted = self.__getPrecoAjustado()
        totalBuy = self.wallet["Compras totais"]
        netResult = totalPriceAdjusted - totalBuy
        self.wallet["Líquido parcial"] = netResult
        self.wallet["Líquido parcial(%)"] = netResult / buyPrice

        # Calculate the ticker percentage per market
        for mkt in market_list:
            self.__setTickerPercentage(mkt)
