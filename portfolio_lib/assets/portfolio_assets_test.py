"""This file is used to test the 'portfolio_assets.py'."""

import os
import sys
from datetime import datetime

import pandas as pd
import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from portfolio_lib.assets.portfolio_assets import PortfolioAssets


def date(string):
    """Return a date from the string."""
    return datetime.strptime(string, "%Y/%m/%d")


class Test_PortfolioAssets_initialization:
    """Tests for 'PortfolioAssets' class: initialization."""

    def test_initialization(self):
        """Test the 'PortfolioAssets': initialization."""
        assets = PortfolioAssets()


class Test_PortfolioAssets_getAdjustedYield:
    """Tests for 'PortfolioAssets' class: getAdjustedYield()."""

    def test_valid_data(self):
        """Test the getAdjustedYield against valid data."""
        assets = PortfolioAssets()
        assert assets.getAdjustedYield(0.0, "IPCA") > 0.0
        assert assets.getAdjustedYield(0.0, "SELIC") > 0.0
        assert assets.getAdjustedYield(0.0, "CDI") == 0.0
        assert assets.getAdjustedYield(0.0, "PREFIXADO") == 0.0

    @pytest.mark.parametrize(
        "yield_val, adjust_type",
        [
            ("CDI", 0.0),
            (0.0, False),
            (False, False),
        ],
    )
    def test_TypeError(self, yield_val, adjust_type):
        """Test the getAdjustedYield against invalid data."""
        assets = PortfolioAssets()
        with pytest.raises(TypeError):
            assets.getAdjustedYield(yield_val, adjust_type)

    @pytest.mark.parametrize(
        "yield_val, adjust_type",
        [
            (0.0, "cdi"),
            (0.0, "selic"),
            (0.0, "ipca"),
            (0.0, "prefixado"),
            (0.0, "A"),
        ],
    )
    def test_ValueError(self, yield_val, adjust_type):
        """Test the getAdjustedYield against invalid data."""
        assets = PortfolioAssets()
        with pytest.raises(ValueError):
            assets.getAdjustedYield(yield_val, adjust_type)


class Test_PortfolioAssets_getColumnsTitleList:
    """Tests for 'PortfolioAssets' class: getColumnsTitleList()."""

    def test_getColumnsTitleList(self):
        """Test the getColumnsTitleList."""
        expected_title_list = [
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
        assets = PortfolioAssets()
        title_list = assets.getColumnsTitleList()
        assert title_list == expected_title_list


class Test_PortfolioAssets_createWalletDefaultColumns:
    """Tests for 'PortfolioAssets' class: createWalletDefaultColumns()."""

    @pytest.mark.parametrize(
        "market_list",
        [
            (["Ações"]),
            (["Opções"]),
            (["FII"]),
            (["BDR"]),
            (["ETF"]),
            (["Renda Fixa"]),
            (["Tesouro Direto"]),
            (["Custodia"]),
            (["Ações", "Opções", "FII", "BDR", "ETF"]),
        ],
    )
    def test_valid_data(self, market_list):
        """Test the createWalletDefaultColumns against valid data."""
        expected_title_list = [
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
        assets = PortfolioAssets()
        df = assets.createWalletDefaultColumns(market_list)
        assert isinstance(df, pd.DataFrame) is True
        assert list(df) == expected_title_list

    @pytest.mark.parametrize(
        "market_list",
        [
            ([]),
            (["Acoes"]),
            (["Acoes", "Opcoes", "fii", "bdr", "etf"]),
        ],
    )
    def test_value_error(self, market_list):
        """Test the createWalletDefaultColumns against invalid data."""
        assets = PortfolioAssets()
        with pytest.raises(ValueError):
            assets.createWalletDefaultColumns(market_list)

    @pytest.mark.parametrize(
        "market_list",
        [
            ([0, 1, 2]),
            (""),
        ],
    )
    def test_type_error(self, market_list):
        """Test the createWalletDefaultColumns against invalid data."""
        assets = PortfolioAssets()
        with pytest.raises(TypeError):
            assets.createWalletDefaultColumns(market_list)
