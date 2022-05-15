"""This file has a set of methods related to Treasuries assets."""

import re

import requests
from bs4 import BeautifulSoup

from portfolio_lib.portfolio_assets import PortfolioAssets


class TreasuriesAssets(PortfolioAssets):
    """Class used to manipulate the Treasuries assets."""

    VALUE_NOT_FOUND = 0.0

    def __init__(self):
        """Create the TreasuriesAssets object."""
        super().__init__()
        self.__initRegexPatterns()

    """Private methods."""

    def __regexCompile(self, stringA, stringB):
        return re.compile(stringA + self.dig4 + stringB + self.dig6)

    def __initRegexPatterns(self):
        # Main link
        self.init_link = r"https://statusinvest.com.br/tesouro/"

        # Regex patterns
        juros = " com Juros Semestrais) "
        self.dig4 = r"(\d\d\d\d)"
        self.dig6 = r"(\d\d\d\d\d\d)"
        self.rxselic = self.__regexCompile(r"(SELIC) ", r"|(LFT) ")
        self.rxpre = self.__regexCompile(r"(Prefixado) ", r"|(LTN) ")
        self.rxprej = self.__regexCompile(r"(Prefixado" + juros, r"|(NTN-F) ")
        self.rxipca = self.__regexCompile(r"(IPCA\+) ", r"|(NTN-B Principal) ")
        self.rxipcaj = self.__regexCompile(r"(IPCA\+" + juros, r"|(NTN-B) ")

        # Regex patterns dictionary
        self.pattern_dict = {
            "SELIC": [
                self.rxselic,
                self.init_link + "tesouro-selic-",
            ],
            "Prefixado": [
                self.rxpre,
                self.init_link + "tesouro-prefixado-",
            ],
            "Prefixado com Juros Semestrais": [
                self.rxprej,
                self.init_link + "tesouro-prefixado-com-juros-semestrais-",
            ],
            "IPCA+": [
                self.rxipca,
                self.init_link + "tesouro-ipca-",
            ],
            "IPCA+ com Juros Semestrais": [
                self.rxipcaj,
                self.init_link + "tesouro-ipca-com-juros-semestrais-",
            ],
        }

    def __getYearPattern(self, rgx, text):
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

    def __getURL(self, text):
        url = False
        for value_list in self.pattern_dict.values():
            rgx = value_list[0]
            link = value_list[1]
            year = self.__getYearPattern(rgx, text)
            if year:
                url = link + year
                break
        return url

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
        self._checkStringType(ticker)

        url = self.__getURL(ticker)

        try:
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
            return float(value)

        except ValueError:
            return TreasuriesAssets.VALUE_NOT_FOUND

        except AttributeError:
            return TreasuriesAssets.VALUE_NOT_FOUND

    def currentTesouroDireto(self):
        """Create a dataframe with all opened operations of Tesouro Direto."""
        self.wallet = self.__currentTesouroDireto()
        return self.wallet.copy()
