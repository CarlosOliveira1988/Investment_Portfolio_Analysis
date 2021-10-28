"""This file provides methods to get fundamental analysis data from stocks."""

import time

import pandas as pd
import yfinance as yf


class FundamentalAnalysisJob:
    """Class useful to collect fundamentalist data from YFinance."""

    def __init__(self):
        """Create the object."""
        pass

    def getTickerDataframe(self, ticker_string):
        """Return a dataframe with more than 150 columns.

        Each column represents an specific parameter such as Price, P/L,
        P/VPA, etc.
        """
        ticker = yf.Ticker(ticker_string)
        columns = list(ticker.info)
        line = list(ticker.info.values())
        return pd.DataFrame([line], columns=columns)

    def getTickerListDataframe(self, tickers_list):
        """Return the dataframe according to the tickers list."""

        def convertValueToDate(df_tickers, column_name):
            """Convert the column values to a datetime format."""

            def setDate(value):
                try:
                    return time.strftime("%Y-%m-%d", time.localtime(value))
                except ValueError:
                    return None

            df_tickers[column_name] = df_tickers[column_name].apply(setDate)

        def calculateRatioAB(df_tickers, column_A, column_B, column_ratio):
            """Return the column with the ratio value."""

            def setRatioColumnValue(value_A, value_B):
                return value_A / value_B

            df_tickers[column_ratio] = df_tickers.apply(
                lambda x: setRatioColumnValue(x[column_A], x[column_B]), axis=1
            )

        # Dataframe of tickers
        df_tickers = pd.DataFrame({})
        df_tickers["LPA"] = ""
        df_tickers["VPA"] = ""

        # Concatenate the new tickers information into the dataframe
        for ticker_string in tickers_list:
            df_new_ticker = self.getTickerDataframe(ticker_string)
            df_tickers = pd.concat(
                [df_tickers, df_new_ticker], ignore_index=True, sort=False
            )

        # Rename the column names and define the order
        rename_dict = {
            "symbol": "Ticker",
            "sector": "Setor",
            "currentPrice": "Preço atual",
            "VPA": "VPA",
            "LPA": "LPA",
            "trailingPE": "P/L",
            "priceToBook": "P/VPA",
            "dividendYield": "Dividend Yield",
            "dividendRate": "Dividendos 12-meses",
            "exDividendDate": "Data ex-dividendos",
            "lastDividendDate": "Data último-dividendo",
            "lastSplitDate": "Data último-split",
        }
        df_tickers = df_tickers.rename(columns=rename_dict)

        # Filter only wished columns
        df_tickers = df_tickers[rename_dict.values()]

        # Set the date column values
        convertValueToDate(df_tickers, "Data ex-dividendos")
        convertValueToDate(df_tickers, "Data último-dividendo")
        convertValueToDate(df_tickers, "Data último-split")

        # Set the ratio column values
        calculateRatioAB(df_tickers, "Preço atual", "P/L", "LPA")
        calculateRatioAB(df_tickers, "Preço atual", "P/VPA", "VPA")

        return df_tickers


class FundamentalAnalysisFrame:
    """Class useful to provide a dataframe with fundamentalistic data."""

    def __init__(self):
        """Create the object."""
        self.tickers_list = None
        self.df_tickers = None
        self.job = FundamentalAnalysisJob()

    def setTickersList(self, tickers_list):
        """Set the tickers list."""
        self.tickers_list = tickers_list

    def getTickersList(self):
        """Get the tickers list."""
        return self.tickers_list

    def updateTickersDataframe(self):
        """Update the dataframe related to the tickers list."""
        self.df_tickers = self.job.getTickerListDataframe(self.tickers_list)

    def getTickersDataframe(self):
        """Get the tickers list dataframe."""
        return self.df_tickers


if __name__ == "__main__":
    frame = FundamentalAnalysisFrame()
    frame.setTickersList(["BBAS3.SA", "ITUB3.SA", "PETR3.SA"])
    frame.updateTickersDataframe()
    df = frame.getTickersDataframe()
    print(df)
