"""This file has a set of methods related to Treasuries assets."""

import re

import requests
from bs4 import BeautifulSoup

from portfolio_lib.portfolio_assets import PortfolioAssets


class TreasuriesAssets(PortfolioAssets):
    """Class used to manipulate the Treasuries assets."""

    def __init__(self):
        """Create the TreasuriesAssets object."""
        super().__init__()

    """Private methods."""

    def __currentTesouroDireto(self):
        # Prepare the default wallet dataframe
        market_list = ["Tesouro Direto"]
        # self.setOpenedOperations(self.openedOperations)
        wallet = self.createWalletDefaultColumns(market_list)

        # Insert the current market values
        for index, row in wallet.iterrows():
            ticker = row["Ticker"]
            wallet.at[index, "Cotação"] = self.currentMarketTesouro(ticker)

        # Calculate values related to the wallet default columns
        self.calculateWalletDefaultColumns(market_list)

        return wallet

    """Public methods."""

    def currentMarketTesouro(self, ticker):
        """Return the last price of the stock from website Status Invest.

        LFT = Letras Financeira do Tesouro
            -> Tesouro Selic
        LTN = Letras do Tesouro Nacional
            -> Tesouro Prefixado sem cupons
        NTN-F = Notas do Tesouro Nacional Tipo F
            -> Tesouro Prefixado com cupons semestrais
        NTN-B Principal = Notas do Tesouro Nacional Tipo B Principal
            -> Tesouro IPCA sem cupons
        NTN-B = Notas do Tesouro Nacional Tipo B
            -> Tesouro IPCA com cupons semestrais
        """
        dig4 = r"(\d\d\d\d)"
        dig6 = r"(\d\d\d\d\d\d)"
        rgx_selic = re.compile(
            r"(SELIC) " + dig4 + "|(LFT) " + dig6,
        )
        rgx_pre = re.compile(
            r"(Prefixado) " + dig4 + "|(LTN) " + dig6,
        )
        rgx_pre_juros = re.compile(
            r"(Prefixado com Juros Semestrais) " + dig4 + "|(NTN-F) " + dig6,
        )
        rgx_ipca = re.compile(
            r"(IPCA\+) " + dig4 + "|(NTN-B Principal) " + dig6,
        )
        rgx_ipca_juros = re.compile(
            r"(IPCA\+ com Juros Semestrais) " + dig4 + "|(NTN-B) " + dig6,
        )

        init_link = r"https://statusinvest.com.br/tesouro/"
        pattern_dict = {
            "SELIC": [
                rgx_selic,
                init_link + "tesouro-selic-",
            ],
            "Prefixado": [
                rgx_pre,
                init_link + "tesouro-prefixado-",
            ],
            "Prefixado com Juros Semestrais": [
                rgx_pre_juros,
                init_link + "tesouro-prefixado-com-juros-semestrais-",
            ],
            "IPCA+": [
                rgx_ipca,
                init_link + "tesouro-ipca-",
            ],
            "IPCA+ com Juros Semestrais": [
                rgx_ipca_juros,
                init_link + "tesouro-ipca-com-juros-semestrais-",
            ],
        }

        def getYearPattern(rgx, text):
            matching = rgx.search(text)
            if matching:
                if matching.group(2):
                    return matching.group(2)
                elif matching.group(4):
                    slc = matching.group(4)[4:]
                    return "20" + slc
                else:
                    return None
            else:
                return None

        def getURL(text):
            url = False
            for value_list in pattern_dict.values():
                rgx = value_list[0]
                link = value_list[1]
                year = getYearPattern(rgx, text)
                if year:
                    url = link + year
                    break
            return url

        value = 0
        url = getURL(ticker)

        if url:
            # Get information from URL
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            # Get the current value from ticker
            value = soup.find(class_="value").get_text()

            # Replace the point to empty in order to transform
            # the string in a number.
            value = value.replace(".", "")

            # Replace comma to point because Python uses point
            # as decimal spacer.
            value = value.replace(",", ".")

        try:
            return float(value)
        except ValueError:
            return 0.0

    def currentTesouroDireto(self):
        """Create a dataframe with all open operations of Tesouro Direto."""
        self.wallet = self.__currentTesouroDireto()
        return self.wallet.copy()
