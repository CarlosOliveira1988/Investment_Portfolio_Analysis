"""This file is used to test the 'treasuries.py'."""

import os
import sys
from datetime import datetime

import pandas as pd
import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from portfolio_lib.treasuries import TreasuriesAssets


def date(string):
    """Return a date from the string."""
    return datetime.strptime(string, "%Y/%m/%d")


class Test_TreasuriesAssets_initialization:
    """Tests for 'TreasuriesAssets' class initialization."""

    def test_initialization(self):
        """Test the 'TreasuriesAssets' initialization."""
        assets = TreasuriesAssets()


class Test_TreasuriesAssets_currentMarketTesouro:
    """Tests for 'TreasuriesAssets' class: currentMarketTesouro()."""

    # List of tuples, with the following order per tuple:
    # - ticker:
    test_currentMarketTesouro_valid_list = [
        ("SELIC 2024"),
        ("LFT 030124"),
        ("Prefixado 2024"),
        ("LTN 010724"),
        ("Prefixado com Juros Semestrais 2027"),
        ("NTN-F 010727"),
        ("IPCA+ 2024"),
        ("NTN-B Principal 150824"),
        ("IPCA+ com Juros Semestrais 2024"),
        ("NTN-B 150824"),
    ]

    # List of tuples, with the following order per tuple:
    # - ticker:
    test_currentMarketTesouro_invalid_list = [
        ("SELIC 1980"),
        ("Prefixado 1980"),
        ("Prefixado com Juros Semestrais 1980"),
        ("IPCA+ 1980"),
        ("IPCA+ com Juros Semestrais 1980"),
        ("A 2000"),
    ]

    @pytest.mark.parametrize("ticker", test_currentMarketTesouro_valid_list)
    def test_currentMarketTesouro_valid_data(self, ticker):
        """Test the 'currentMarketTesouro' method against valid data."""
        assets = TreasuriesAssets()
        val = assets.currentMarketTesouro(ticker)
        assert isinstance(val, float) is True

    @pytest.mark.parametrize("ticker", test_currentMarketTesouro_invalid_list)
    def test_currentMarketTesouro_invalid_data(self, ticker):
        """Test the 'currentMarketTesouro' method against invalid data."""
        assets = TreasuriesAssets()
        val = assets.currentMarketTesouro(ticker)
        assert isinstance(val, float) is True
        assert 0.0 == pytest.approx(val, 0.001)

    def test_currentMarketPriceByTicker_typeerror(self):
        """Test the 'currentMarketPriceByTicker' against invalid data."""
        assets = TreasuriesAssets()
        with pytest.raises(TypeError):
            assets.currentMarketTesouro(0)


class Test_TreasuriesAssets_currentTesouroDireto:
    """Tests for 'TreasuriesAssets' class: currentTesouroDireto()."""

    def test_currentTesouroDireto(self):
        """Test the 'TreasuriesAssets' class: currentTesouroDireto()."""
        expected_title_list = [
            "Ticker",
            "Mercado",
            "Indexador",
            "Rentabilidade-média Contratada",
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
        assets = TreasuriesAssets()
        title_list = list(assets._getDefaultDataframe())
        df = assets.currentTesouroDireto()
        assert isinstance(df, pd.DataFrame) is True
        assert all(item in title_list for item in list(df)) is True
        assert title_list == expected_title_list
