"""File used to collect 12months-base data from Economic Indexers."""

import requests
from bs4 import BeautifulSoup


class Indexer:
    """
    Class used to get IPCA and CDI 12months-base % value.

    It uses the Status Invest website. IPCA and CDI shares the same selector.
    """

    VALUE_NOT_FOUND = 0.0

    def __init__(self, indexer_string):
        """Create the Indexer object."""
        self.weblink = r"https://statusinvest.com.br/" + str(indexer_string)
        self.selector = (
            "#indexer > div > div:nth-child(1) > div > "
            + "div.info.special.w-100.w-sm-33.w-md-25 > div > div:nth-child(1)"
            + "> strong"
        )
        self.value = self.__getUpdatedData()

    def __getUpdatedData(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(self.weblink, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        selector = soup.select(self.selector)
        try:
            value_str = selector[0].get_text()
            value = value_str.replace(",", ".")
            return float(value) / 100
        except IndexError:
            return Indexer.VALUE_NOT_FOUND
        except ValueError:
            return Indexer.VALUE_NOT_FOUND

    def get12MonthsValue(self):
        """Return the 12months-base % value."""
        return self.value


class TwelveMonthsIndexer:
    """
    Class used to get IPCA and CDI 12months-base % value.

    It uses the Status Invest website. IPCA and CDI shares the same selector.
    """

    def __init__(self):
        """Create the TwelveMonthsIndexer object."""
        self.IPCA = Indexer("ipca")
        self.CDI = Indexer("cdi")

    def getIPCA(self):
        """Return the IPCA 12months-base % value."""
        return self.IPCA.get12MonthsValue()

    def getCDI(self):
        """Return the CDI 12months-base % value."""
        return self.CDI.get12MonthsValue()

    def getSELIC(self):
        """Return the SELIC 12months-base % value."""
        # Since CDI~SELIC, we will return the CDI value
        return self.CDI.get12MonthsValue()
