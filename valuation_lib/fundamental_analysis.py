"""This file provides methods to get fundamental analysis data from stocks."""

import pandas as pd

from portfolio_lib.assets.status_invest import HtmlCacheManager, LocalScraper


class FundamentalAnalysisJob:
    """Class useful to collect fundamentalist data from YFinance."""

    def __init__(self):
        """Create the object."""
        self._scraper = LocalScraper()
        self._cache = HtmlCacheManager()

    def getTickerListDataframe(self, tickers_list, markets_list):
        """Return the dataframe according to the tickers list."""
        self._cache.register_local_time()

        df_tickers = pd.DataFrame({})

        # Concatenate the new tickers information into the dataframe
        for ticker, market in zip(tickers_list, markets_list):

            # Donwload new data if necessary
            self._cache.set_ticker_market(ticker, market)
            if self._cache.is_ticker_cache_not_updated():
                self._cache.download_new_ticker_data()

            ticker_path = self._cache.get_ticker_cache_file_path()
            self._scraper.set_html_file_properties(ticker_path, ticker, market)

            df_new_ticker = self._scraper.get_dataframe()
            df_tickers = pd.concat(
                [df_tickers, df_new_ticker], ignore_index=True, sort=False
            )

        return df_tickers


class FundamentalAnalysisFrame:
    """Class useful to provide a dataframe with fundamentalistic data."""

    def __init__(self):
        """Create the object."""
        self.tickers_list = None
        self.markets_list = None
        self.df_tickers = None
        self.job = FundamentalAnalysisJob()

    def setTickersList(self, tickers_list, markets_list):
        """Set the tickers list."""
        self.tickers_list = tickers_list
        self.markets_list = markets_list

    def getTickersList(self):
        """Get the tickers list."""
        return self.tickers_list

    def getMarketsList(self):
        """Get the markets list."""
        return self.markets_list

    def updateTickersDataframe(self):
        """Update the dataframe related to the tickers list."""
        self.df_tickers = self.job.getTickerListDataframe(
            self.tickers_list,
            self.markets_list,
        )

    def getTickersDataframe(self):
        """Get the tickers list dataframe."""
        return self.df_tickers


if __name__ == "__main__":
    frame = FundamentalAnalysisFrame()
    frame.setTickersList(
        ["BBAS3", "AMZO34", "HASH11", "CPTS11", "TESOURO IPCA+ 2026"],
        ["Ações", "BDR", "ETF", "FII", "Tesouro Direto"],
    )
    frame.updateTickersDataframe()
    df = frame.getTickersDataframe()
    print(df)
