"""This file has a set of methods related to Variable Income assets."""

import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup

from portfolio_lib.gdrive_exporter import GoogleDriveExporter
from portfolio_lib.multi_processing import PoolTasks
from portfolio_lib.portfolio_assets import PortfolioAssets


class VariableIncomeAssets(PortfolioAssets):
    """Class used to manipulate the Variable Income assets."""

    SECTOR_NOT_FOUND = "Sector not found"
    VALUE_NOT_FOUND = 0.0

    def __init__(self):
        """Create the VariableIncomeAssets object."""
        super().__init__()
        self.wallet = self.__renameColumns(self.wallet)
        self.openedOperations = self.__renameColumns(self.openedOperations)

    """Private methods."""

    def __renameColumns(self, dataframe):
        col, dataframe = self.__renameYieldColumn(dataframe)
        return dataframe

    def __renameYieldColumn(self, wallet):
        default_yield_col = "Taxa-média Contratada"
        yield_col = "Dividend-Yield Ajustado"
        dict_rename = {default_yield_col: yield_col}
        wallet = wallet.rename(columns=dict_rename, inplace=False)
        return yield_col, wallet

    def __currentPortfolio(self):
        # Prepare the default wallet dataframe
        market_list = ["Ações", "ETF", "FII", "BDR"]
        # self.setOpenedOperations(self.openedOperations)
        wallet = self.createWalletDefaultColumns(market_list)

        # Create a list of ticker to be used in YFinance API
        listTicker = wallet["Ticker"].tolist()
        listTicker = [(Ticker + ".SA") for Ticker in listTicker]
        listMarket = wallet["Mercado"].tolist()

        # Get related values of all tickers in the wallet
        if listTicker:

            # Get the current values of all tickers in the wallet
            curPricesTickers = self.currentMarketPriceByTickerList(listTicker)
            for index, row in wallet.iterrows():
                # ".SA" is needed due YFinance
                ticker = row["Ticker"] + ".SA"
                wallet.at[index, "Cotação"] = float(curPricesTickers[ticker])

            # Get the current dividend yield of all tickers in the wallet
            yield_col = "Taxa-média Contratada"
            yield_df = self.currentMarketYieldByTickerList(
                listTicker,
                listMarket,
            )
            for index, row in wallet.iterrows():
                # ".SA" is needed due YFinance
                ticker = row["Ticker"] + ".SA"
                wallet.at[index, yield_col] = float(yield_df[ticker])

        # Calculate values related to the wallet default columns
        self.calculateWalletDefaultColumns(market_list)

        # Calculate the adjusted dividend yield
        yield_col, wallet = self.__renameYieldColumn(wallet)
        yield_val = wallet[yield_col] * wallet["Preço mercado"]
        wallet[yield_col] = yield_val / wallet["Preço pago"]

        return wallet

    def __getSectorOfTicker(self, ticker):
        data = yf.Ticker(ticker)
        return data.info["sector"]

    def __getCurrentMarketPriceByTicker(self, ticker):
        # I had issues when downloading data for Fundos imobiliários.
        # It was necessary to work with period of 30d.
        # I believe that is mandatory period or start/end date.
        # With start/end I also had issues for reading the values.
        # The solution was to consider "30d" as the period.
        # I compared the results from function in Google and they were correct.
        try:
            dataframe = yf.download(ticker, period="30d")
            data = dataframe["Adj Close"].tail(1)
            return float(data)
        except TypeError:
            return VariableIncomeAssets.VALUE_NOT_FOUND

    """Protected methods."""

    def _currentMarketYieldByTicker(self, arg_list):
        ticker = arg_list[0]
        market = arg_list[1]
        return [self.currentMarketYieldByTicker(ticker, market)]

    def _checkMarketType(self, market):
        self._checkStringType(market)
        if market not in ["Ações", "FII", "BDR", "ETF"]:
            raise ValueError(
                "The market argument should be 'Ações', 'FII', 'BDR', 'ETF'.",
            )

    def _checkMarketListType(self, market_list):
        self._checkStringListType(market_list)
        [self._checkMarketType(market) for market in market_list]

    def _getDefaultDataframe(self):
        dataframe = self._getAssetsDefaultDataframe()
        yield_col, dataframe = self.__renameYieldColumn(dataframe)
        return dataframe

    """Public methods."""

    def sectorOfTicker(self, ticker):
        """Return the sector of a given ticker.

        The function uses the yfinance library to get the information.
        """
        self._checkStringType(ticker)
        try:
            return self.__getSectorOfTicker(ticker)
        except KeyError:
            try:
                return self.__getSectorOfTicker(ticker + ".SA")
            except KeyError:
                return VariableIncomeAssets.SECTOR_NOT_FOUND

    def currentMarketPriceByTicker(self, ticker):
        """Return the last price of a given ticker.

        The function uses the yfinance library to get the information.
        """
        self._checkStringType(ticker)
        try:
            return self.__getCurrentMarketPriceByTicker(ticker)
        except KeyError:
            try:
                return self.__getCurrentMarketPriceByTicker(ticker + ".SA")
            except KeyError:
                return VariableIncomeAssets.VALUE_NOT_FOUND

    def currentMarketYieldByTicker(self, ticker, market):
        """Return the current Dividend Yield of a given ticker and market.

        The available type of markets are:
        - Ações
        - FII
        - BDR
        - ETF

        The function uses the Status Invest website to get the information.
        """
        self._checkStringType(ticker)
        self._checkMarketType(market)
        # During some performance tests, I noticed this is the
        # slowest function related to RendaVariavel type.
        # If we want to improve the application performance, we need to change
        # something here.

        # Prepare the URL
        strip_list = ticker.split(".")  # The left side is without ".SA"
        true_ticker = strip_list[0]
        main_url = "https://statusinvest.com.br/"
        if market == "FII":
            url = main_url + "fundos-imobiliarios/" + true_ticker
        else:
            url = main_url + "acoes/" + true_ticker

        # Web scraping
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        if market == "FII":
            selector = soup.select(
                "#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap."
                + "justify-between.mb-3.mb-md-5 > div:nth-child(4) > div > div"
                + ":nth-child(1) > strong"
            )
        else:
            selector = soup.select(
                "#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div >"
                + " div:nth-child(4) > div > div:nth-child(1) > strong"
            )

        # Convert string to float values
        try:
            value_str = selector[0].get_text()
            value = value_str.replace(",", ".")
            return float(value) / 100
        except IndexError:
            return VariableIncomeAssets.VALUE_NOT_FOUND
        except ValueError:
            return VariableIncomeAssets.VALUE_NOT_FOUND

    def currentMarketPriceByTickerList(self, value_list):
        """Return a dataframe with the last price of the stocks in the list.

        The function uses the yfinance library to get the information.
        """
        self._checkStringListType(value_list)

        # The 'tail' method returns a 'pandas.series'
        # when exists only 1 ticker in the variable 'list'.
        dataframe = yf.download(value_list, period="1d")
        data = dataframe["Adj Close"].tail(1)

        # In order to solve the '1 ticker' case and return always
        # a 'pandas.dataframe' with the ticker name, we need to convert
        # the 'pandas.series' to a 'pandas.dataframe' and adjust its
        # column name.
        try:
            data = data.to_frame()
            if len(data) == 1:
                data = data.rename(columns={"Adj Close": value_list[0]})
        except AttributeError:
            data = data
        return data

    def currentMarketYieldByTickerList(self, tickerList, marketList):
        """Return a dataframe with the current Dividend Yield.

        The available type of markets are:
        - Ações
        - FII
        - BDR
        - ETF

        The function uses the Status Invest website to get the information
        """
        self._checkStringListType(tickerList)
        self._checkMarketListType(marketList)
        # Set the pool list variables
        self.tickerPool = []
        self.marketPool = []
        self.yieldPool = []
        for index, ticker in enumerate(tickerList):
            self.tickerPool.append(ticker)
            self.marketPool.append(marketList[index])
            self.yieldPool.append([])
        self.indexPool = range(len(self.yieldPool))

        # Run the pool multitask
        self.yieldPool = PoolTasks().runPool(
            self._currentMarketYieldByTicker,
            zip(
                self.tickerPool,
                self.marketPool,
                self.indexPool,
            ),
        )
        df_dict = dict(zip(self.tickerPool, self.yieldPool))
        return pd.DataFrame(data=df_dict)

    def currentPortfolio(self):
        """Analyze the operations to get the current wallet.

        Return a dataframe containing the current wallet of stocks, FIIs,
        ETFs and BDRs.
        """
        self.wallet = self.__currentPortfolio()
        return self.wallet.copy()

    def currentPortfolioGoogleDrive(
        self,
        extrato_path,
        auto_save=True,
        auto_open=True,
    ):
        """Save the excel file to be used in Google Drive."""
        exporter = GoogleDriveExporter()
        return exporter.save(
            self.wallet.copy(),
            extrato_path,
            auto_save,
            auto_open,
        )
