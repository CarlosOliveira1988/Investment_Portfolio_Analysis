"""This file is used to test the 'variable_income.py'."""

import os
import sys

import pandas as pd
import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from portfolio_lib.variable_income import VariableIncomeAssets


class Test_VariableIncomeAssets_initialization:
    """Tests for 'VariableIncomeAssets' class initialization."""

    def test_initialization(self):
        """Test the 'VariableIncomeAssets' initialization."""
        assets = VariableIncomeAssets()


class Test_VariableIncomeAssets_sectorOfTicker:
    """Tests for 'VariableIncomeAssets' class: sectorOfTicker()."""

    # List of tuples, with the following order per tuple:
    # - ticker:
    test_sectorOfTicker_valid_list = [
        # Stocks, FIIs, ETFs, BDRs, invalid string
        ("BBAS3"),
        ("CPTS11"),
        ("HASH11"),
        ("AMZO34"),
        ("DCBAXS"),
    ]

    @pytest.mark.parametrize(
        "ticker",
        test_sectorOfTicker_valid_list,
    )
    def test_sectorOfTicker_valid_data(self, ticker):
        """Test the 'sectorOfTicker' method against valid data."""
        assets = VariableIncomeAssets()
        val = assets.sectorOfTicker(ticker)
        assert isinstance(val, str) is True

    def test_sectorOfTicker_not_valid_data(self):
        """Test the 'sectorOfTicker' method against not valid data."""
        assets = VariableIncomeAssets()
        with pytest.raises(TypeError):
            assets.sectorOfTicker(0)


class Test_VariableIncomeAssets_currentMarketPriceByTicker:
    """Tests for 'VariableIncomeAssets' class: currentMarketPriceByTicker()."""

    # List of tuples, with the following order per tuple:
    # - ticker:
    test_currentMarketPriceByTicker_valid_list = [
        # Stocks, FIIs, ETFs, BDRs, invalid string
        ("BBAS3"),
        ("CPTS11"),
        ("HASH11"),
        ("AMZO34"),
        ("DCBAXS"),
    ]

    @pytest.mark.parametrize(
        "ticker",
        test_currentMarketPriceByTicker_valid_list,
    )
    def test_currentMarketPriceByTicker_valid_data(self, ticker):
        """Test the 'currentMarketPriceByTicker' method against valid data."""
        assets = VariableIncomeAssets()
        val = assets.currentMarketPriceByTicker(ticker)
        assert isinstance(val, float) is True

    def test_currentMarketPriceByTicker_not_valid_data(self):
        """Test the 'currentMarketPriceByTicker' against invalid data."""
        assets = VariableIncomeAssets()
        with pytest.raises(TypeError):
            assets.currentMarketPriceByTicker(0)


class Test_VariableIncomeAssets_currentMarketYieldByTicker:
    """Tests for 'VariableIncomeAssets' class: currentMarketYieldByTicker()."""

    # List of tuples, with the following order per tuple:
    # - ticker, market:
    test_currentMarketYieldByTicker_valid_list = [
        # Stocks, FIIs, ETFs, BDRs, invalid string
        ("BBAS3", "Ações"),
        ("CPTS11", "FII"),
        ("HASH11", "ETF"),
        ("AMZO34", "BDR"),
    ]

    # List of tuples, with the following order per tuple:
    # - ticker, market:
    test_currentMarketYieldByTicker_typeerror_list = [
        # Stocks, FIIs, ETFs, BDRs, invalid string
        (0, 0),
        ("BBAS3", 0),
        (0, "Ações"),
    ]

    # List of tuples, with the following order per tuple:
    # - ticker, market:
    test_currentMarketYieldByTicker_valueerror_list = [
        # Stocks, FIIs, ETFs, BDRs, invalid string
        ("BBAS3", "Acoes"),
        ("BBAS3", "FIIs"),
        ("BBAS3", "ETFs"),
        ("BBAS3", "BDRs"),
        ("BBAS3", "a"),
        ("a", "BBAS3"),
    ]

    @pytest.mark.parametrize(
        "ticker, market",
        test_currentMarketYieldByTicker_valid_list,
    )
    def test_currentMarketYieldByTicker_valid_data(self, ticker, market):
        """Test the 'currentMarketYieldByTicker' method against valid data."""
        assets = VariableIncomeAssets()
        val = assets.currentMarketYieldByTicker(ticker, market)
        assert isinstance(val, float) is True

    @pytest.mark.parametrize(
        "ticker, market",
        test_currentMarketYieldByTicker_typeerror_list,
    )
    def test_currentMarketYieldByTicker_typeerror(self, ticker, market):
        """Test the 'currentMarketYieldByTicker' against invalid data."""
        assets = VariableIncomeAssets()
        with pytest.raises(TypeError):
            assets.currentMarketYieldByTicker(ticker, market)

    @pytest.mark.parametrize(
        "ticker, market",
        test_currentMarketYieldByTicker_valueerror_list,
    )
    def test_currentMarketYieldByTicker_valueerror(self, ticker, market):
        """Test the 'currentMarketYieldByTicker' against invalid data."""
        assets = VariableIncomeAssets()
        with pytest.raises(ValueError):
            assets.currentMarketYieldByTicker(ticker, market)


class Test_VariableIncomeAssets_currentMarketPriceByTickerList:
    """Tests for 'VariableIncomeAssets': currentMarketPriceByTickerList()."""

    # List of tuples, with the following order per tuple:
    # - ticker:
    test_currentMarketPriceByTickerList_valid_list = [
        # Ticker list:
        # - Stock
        # - FII
        # - ETF
        # - BDR
        # - invalid string
        (["BBAS3"]),
        (["BBAS3", "CPTS11", "HASH11", "AMZO34"]),
        (["BBAS3", "CPTS11", "HASH11", "AMZO34", "DCBAXS"]),
        (["A", "B", "C", "D", "E"]),
    ]

    # List of tuples, with the following order per tuple:
    # - ticker:
    test_currentMarketPriceByTickerList_typeerror_list = [
        # Ticker list:
        # - Stock
        # - FII
        # - ETF
        # - BDR
        # - invalid string
        ("BBAS3"),
        ([0, "BBAS3", None, True, []]),
    ]

    @pytest.mark.parametrize(
        "ticker_list",
        test_currentMarketPriceByTickerList_valid_list,
    )
    def test_currentMarketPriceByTickerList_valid_data(self, ticker_list):
        """Test the 'currentMarketPriceByTickerList' against valid data."""
        assets = VariableIncomeAssets()
        val = assets.currentMarketPriceByTickerList(ticker_list)
        assert isinstance(val, pd.DataFrame) is True

    @pytest.mark.parametrize(
        "ticker_list",
        test_currentMarketPriceByTickerList_typeerror_list,
    )
    def test_currentMarketPriceByTickerList_typeerror(self, ticker_list):
        """Test the 'currentMarketPriceByTickerList' against invalid data."""
        assets = VariableIncomeAssets()
        with pytest.raises(TypeError):
            assets.currentMarketPriceByTickerList(ticker_list)

    def test_currentMarketPriceByTickerList_valueerror(self):
        """Test the 'currentMarketPriceByTickerList' against invalid data."""
        assets = VariableIncomeAssets()
        with pytest.raises(ValueError):
            assets.currentMarketPriceByTickerList([])


class Test_VariableIncomeAssets_currentMarketYieldByTickerList:
    """Tests for 'VariableIncomeAssets': currentMarketYieldByTickerList()."""

    # List of tuples, with the following order per tuple:
    # - ticker_list, market_list:
    test_currentMarketYieldByTickerList_valid_list = [
        (["A"], ["Ações"]),
        (["BBAS3"], ["Ações"]),
        (["CPTS11"], ["FII"]),
        (["HASH11"], ["ETF"]),
        (["AMZO34"], ["BDR"]),
    ]

    # List of tuples, with the following order per tuple:
    # - ticker_list, market_list:
    test_currentMarketYieldByTickerList_typeerror_list = [
        (["A"], [0]),
        ([0], ["A"]),
        ([0], [0]),
        (0, 0),
    ]

    # List of tuples, with the following order per tuple:
    # - ticker_list, market_list:
    test_currentMarketYieldByTickerList_valueerror_list = [
        (["A"], ["Acoes"]),
        (["A"], ["FIIs"]),
        (["A"], ["BDRs"]),
        (["A"], ["ETFs"]),
    ]

    @pytest.mark.parametrize(
        "ticker_list, market_list",
        test_currentMarketYieldByTickerList_valid_list,
    )
    def test_currentMarketYieldByTickerList_valid_data(
        self,
        ticker_list,
        market_list,
    ):
        """Test the 'currentMarketYieldByTickerList' against valid data."""
        assets = VariableIncomeAssets()
        val = assets.currentMarketYieldByTickerList(ticker_list, market_list)
        assert isinstance(val, pd.DataFrame) is True

    @pytest.mark.parametrize(
        "ticker_list, market_list",
        test_currentMarketYieldByTickerList_typeerror_list,
    )
    def test_currentMarketYieldByTickerList_typeerror(
        self,
        ticker_list,
        market_list,
    ):
        """Test the 'currentMarketYieldByTickerList' against invalid data."""
        assets = VariableIncomeAssets()
        with pytest.raises(TypeError):
            assets.currentMarketYieldByTickerList(ticker_list, market_list)

    @pytest.mark.parametrize(
        "ticker_list, market_list",
        test_currentMarketYieldByTickerList_valueerror_list,
    )
    def test_currentMarketYieldByTickerList_valueerror(
        self,
        ticker_list,
        market_list,
    ):
        """Test the 'currentMarketYieldByTickerList' against invalid data."""
        assets = VariableIncomeAssets()
        with pytest.raises(ValueError):
            assets.currentMarketYieldByTickerList(ticker_list, market_list)


class Test_VariableIncomeAssets_currentPortfolio:
    """Tests for 'VariableIncomeAssets': currentPortfolio()."""

    def test_currentPortfolio(self):
        """Test the 'VariableIncomeAssets' class: currentPortfolio()."""
        expected_title_list = [
            "Ticker",
            "Mercado",
            "Indexador",
            "Dividend-Yield",
            "Dividend-Yield Ajustado",
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
        assets = VariableIncomeAssets()
        title_list = list(assets._getDefaultDataframe())
        df = assets.currentPortfolio()
        assert isinstance(df, pd.DataFrame) is True
        assert all(item in title_list for item in list(df)) is True
        assert title_list == expected_title_list
