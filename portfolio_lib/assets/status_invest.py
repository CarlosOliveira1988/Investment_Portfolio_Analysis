"""File useful to get several stock parameters from Status Invest."""

import locale
import os
import time
import urllib.request
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

from portfolio_lib.assets.selector_bdrs import BDRS_HTML_SELECTOR_DICT as bdrs_selector
from portfolio_lib.assets.selector_etfs import ETFS_HTML_SELECTOR_DICT as etfs_selector
from portfolio_lib.assets.selector_fiis import FIIS_HTML_SELECTOR_DICT as fiis_selector
from portfolio_lib.assets.selector_stocks import (
    STOCKS_HTML_SELECTOR_DICT as stocks_selector,
)
from portfolio_lib.assets.selector_tesouro import (
    TESOURO_HTML_SELECTOR_DICT as tesouro_selector,
)
from portfolio_lib.assets.treasuries import TreasuriesAssets


class HtmlCacheManager:
    """Class used to manage HTML files for caching purpose."""

    STATUS_INVEST_URL = r"https://statusinvest.com.br/"

    TEMP_FOLDER_PATH = r"\portfolio_lib\assets\temp"

    TIME_IN_MINUTES_FOR_CACHING = 15
    TIME_IN_SECONDS_FOR_CACHING = TIME_IN_MINUTES_FOR_CACHING * 60

    def __init__(self):
        """Cheate the HtmlCacheManager object."""
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

        self._current_directory = os.path.abspath(os.path.curdir)
        self._temporary_folder_path = os.path.join(
            self._current_directory,
            "portfolio_lib",
            "assets",
            "temp",
        )
        self._create_temp_folder_if_not_exists()

        self._market = None
        self._ticker = None
        self._ticker_cache_path = None
        self._ticker_url = None

        self._url_opener = urllib.request.URLopener()
        self._url_opener.addheader("User-Agent", "Mozilla/5.0")

        self._treasuries_assets = TreasuriesAssets()

        self.register_local_time()

    def _create_temp_folder_if_not_exists(self):
        if not os.path.isdir(self._temporary_folder_path):
            os.makedirs(self._temporary_folder_path)

    def _get_ticker_url(self, ticker, market):
        """Get the URL related to the wished ticker."""
        main_url = HtmlCacheManager.STATUS_INVEST_URL
        if market == "FII":
            return main_url + "fundos-imobiliarios/" + ticker
        elif market == "ETF":
            return main_url + "etfs/" + ticker
        elif market == "Ações":
            return main_url + "acoes/" + ticker
        elif market == "BDR":
            return main_url + "bdrs/" + ticker
        elif market == "Tesouro Direto":
            return self._treasuries_assets._getURL(ticker)

    def _get_ticker_cache_path(self, ticker):
        """Get the path where the ticker cache is stored."""
        return os.path.join(self._temporary_folder_path, ticker + ".html")

    def _get_ticker_cache_modified_time(self, ticker_cache_path):
        """Get the date time when the ticker cache was saved."""
        mtime = os.path.getmtime(ticker_cache_path)
        return datetime.fromtimestamp(mtime)

    def _get_diff_to_local_time_in_seconds(self, ticker_cache_time):
        """Return the difference between 2 times, in seconds."""
        return (self._local_time - ticker_cache_time).total_seconds()

    def _ticker_cache_exists(self, ticker_cache_path):
        """Return True if the cache file already exists."""
        return os.path.isfile(ticker_cache_path)

    """Public methods."""

    def register_local_time(self):
        """Return the local time."""
        self._local_time = datetime.now()

    def is_ticker_cache_not_updated(self):
        """Return True if the cache is not updated according to the time.

        Return True if the cache file does not exist.
        """
        if self._ticker_cache_exists(self._ticker_cache_path):
            cache_time = self._get_ticker_cache_modified_time(self._ticker_cache_path)
            diff_time = self._get_diff_to_local_time_in_seconds(cache_time)
            return diff_time > HtmlCacheManager.TIME_IN_SECONDS_FOR_CACHING
        else:
            return True

    def download_new_ticker_data(self):
        """Download the new ticker data and store in the cache temp folder."""
        self._url_opener.retrieve(self._ticker_url, self._ticker_cache_path)
        print("donwloading new data for", self._ticker, ":", self._market)

    def set_ticker_market(self, ticker, market):
        """Set the ticker and market."""
        self._ticker_cache_path = self._get_ticker_cache_path(ticker)
        self._ticker_url = self._get_ticker_url(ticker, market)
        self._market = market
        self._ticker = ticker

    def get_ticker_cache_file_path(self):
        """Return the cache file path."""
        return self._ticker_cache_path


class LocalScraper:
    """Class used to get values from local HTML pages."""

    def __init__(self):
        """Create the LocalScraper object."""
        self._soup = None
        self._selector_dict = None
        self._ticker = None
        self._market = None

    def _get_text_from_selector(self, selector_str):
        """Return the scraped text."""
        if selector_str:
            selector = self._soup.select(selector_str)
            return selector[0].get_text()
        else:
            return "0,00"

    def _get_float_from_string_selector(self, selector_str, divide_by=1.0):
        """Get the float value from a string.

        Example: get the '4.1706' from '4,1706'
        """
        value_str = self._get_text_from_selector(selector_str)
        value_str = value_str.replace(".", "")
        value_str = value_str.replace("R$ ", "")
        value_str = value_str.replace("%", "")
        value = value_str.replace(",", ".")
        return float(value) / divide_by

    """Public methods."""

    def set_html_file_properties(self, local_html_file, ticker, market):
        """Set the HTML file and prepare the BeautifulSoup."""
        self._soup = BeautifulSoup(
            open(local_html_file, encoding="utf8"),
            "html.parser",
        )
        if market == "FII":
            self._selector_dict = fiis_selector
        elif market == "ETF":
            self._selector_dict = etfs_selector
        elif market == "Ações":
            self._selector_dict = stocks_selector
        elif market == "BDR":
            self._selector_dict = bdrs_selector
        elif market == "Tesouro Direto":
            self._selector_dict = tesouro_selector
        self._ticker = ticker
        self._market = market

    def get_current_price(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Valor atual"],
        )

    def get_price_change_in_day(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Variação no dia"],
            divide_by=100,
        )

    def get_min_price_in_month(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Min. no mês"],
        )

    def get_max_price_in_month(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Máx. no mês"],
        )

    def get_price_change_in_month(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Variação no mês"],
            divide_by=100,
        )

    def get_min_price_in_52_weeks(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Min. 52 semanas"],
        )

    def get_max_price_in_52_weeks(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Máx. 52 semanas"],
        )

    def get_price_change_in_12_months(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Variação 12 meses"],
            divide_by=100,
        )

    def get_dividend_yield(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Dividend yield"],
            divide_by=100,
        )

    def get_dividend_12_months(self):
        return self._get_float_from_string_selector(
            self._selector_dict["Dividendos 12 meses"],
        )

    def get_P_L_index(self):
        return self._get_float_from_string_selector(
            self._selector_dict["P/L"],
        )

    def get_P_VP_index(self):
        return self._get_float_from_string_selector(
            self._selector_dict["P/VP"],
        )

    def get_VPA_index(self):
        return self._get_float_from_string_selector(
            self._selector_dict["VPA"],
        )

    def get_LPA_index(self):
        return self._get_float_from_string_selector(
            self._selector_dict["LPA"],
        )

    def get_dataframe(self):
        data_dict = {
            "Ticker": [self._ticker],
            "Mercado": [self._market],
            "Valor atual": [self.get_current_price()],
            "Variação no dia": [self.get_price_change_in_day()],
            "Min. no mês": [self.get_min_price_in_month()],
            "Máx. no mês": [self.get_max_price_in_month()],
            "Variação no mês": [self.get_price_change_in_month()],
            "Min. 52 semanas": [self.get_min_price_in_52_weeks()],
            "Máx. 52 semanas": [self.get_max_price_in_52_weeks()],
            "Variação 12 meses": [self.get_price_change_in_12_months()],
            "Dividend yield": [self.get_dividend_yield()],
            "Dividendos 12 meses": [self.get_dividend_12_months()],
            "P/L": [self.get_P_L_index()],
            "P/VP": [self.get_P_VP_index()],
            "VPA": [self.get_VPA_index()],
            "LPA": [self.get_LPA_index()],
        }
        return pd.DataFrame(data=data_dict)
