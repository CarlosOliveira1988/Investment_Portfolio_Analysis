"""This file is used to test the 'fixed_income.py'."""

import os
import sys
from datetime import datetime

import pandas as pd
import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from portfolio_lib.fixed_income import FixedIncomeAssets


def date(string):
    """Return a date from the string."""
    return datetime.strptime(string, "%Y/%m/%d")


class Test_FixedIncomeAssets_initialization:
    """Tests for 'FixedIncomeAssets' class initialization."""

    def test_initialization(self):
        """Test the 'FixedIncomeAssets' initialization."""
        assets = FixedIncomeAssets()


class Test_FixedIncomeAssets_currentValRendaFixa_validData:
    """Tests for 'FixedIncomeAssets' class: currentValRendaFixa()."""

    # List of tuples, with the following order per tuple:
    # - inidate, enddate, indexer, rate, buy, result
    test_currentValRendaFixa_valid_list = [
        # Fixed Income Investment does not generate income in the 1st day.
        (date("2000/01/01"), date("2000/01/01"), "PREFIXADO", 1.0, 100, 0.0),
        (date("2000/01/01"), date("2000/01/01"), "IPCA", 1.0, 100, 0.0),
        (date("2000/01/01"), date("2000/01/01"), "CDI", 1.0, 100, 0.0),
        # Fixed Income Investment generates incomes related to 1 month.
        (date("2000/01/01"), date("2000/01/31"), "PREFIXADO", 0.1, 100, 0.797),
        (date("2000/01/01"), date("2000/01/31"), "IPCA", 0.0, 100, 0.62),
        (date("2000/01/01"), date("2000/01/31"), "CDI", 1.0, 100, 1.44),
        # Fixed Income Investment generates incomes related to 1 year.
        (date("2000/01/01"), date("2000/12/31"), "PREFIXADO", 0.1, 100, 10.0),
        (date("2000/01/01"), date("2000/12/31"), "IPCA", 0.0, 100, 5.97),
        (date("2000/01/01"), date("2000/12/31"), "CDI", 1.0, 100, 17.32),
    ]

    @pytest.mark.parametrize(
        "inidate, enddate, indexer, rate, buy, result",
        test_currentValRendaFixa_valid_list,
    )
    def test_currentValRendaFixa_valid_data(
        self, inidate, enddate, indexer, rate, buy, result
    ):
        """Test the 'currentValRendaFixa' method against valid data."""
        assets = FixedIncomeAssets()
        val = assets.currentValRendaFixa(inidate, enddate, indexer, rate, buy)
        assert result == pytest.approx((val - buy), 0.001)


class Test_FixedIncomeAssets_currentValRendaFixa_TypeErrors:
    """Tests for 'FixedIncomeAssets' class: currentValRendaFixa()."""

    # List of tuples, with the following order per tuple:
    # - inidate, enddate, indexer, rate, buy
    test_currentValRendaFixa_invalid_date_list = [
        # Invalid date types should raise TypeError exceptions
        (date("2000/01/01"), "2000/01/01", "PREFIXADO", 1.0, 100),
        ("2000/01/01", date("2000/01/01"), "PREFIXADO", 1.0, 100),
        # Invalid rate and buyPrice types should raise TypeError exceptions
        (date("2000/01/01"), date("2000/01/01"), "PREFIXADO", "1.0", 100),
        (date("2000/01/01"), date("2000/01/01"), "PREFIXADO", 1.0, "100"),
        # Invalid indexer type should raise TypeError exceptions
        (date("2000/01/01"), date("2000/01/01"), 0, 1.0, 100),
    ]

    @pytest.mark.parametrize(
        "inidate, enddate, indexer, rate, buy",
        test_currentValRendaFixa_invalid_date_list,
    )
    def test_currentValRendaFixa_invalid_dates(
        self, inidate, enddate, indexer, rate, buy
    ):
        """Test the 'currentValRendaFixa' method against invalid dates."""
        assets = FixedIncomeAssets()
        with pytest.raises(TypeError):
            assets.currentValRendaFixa(inidate, enddate, indexer, rate, buy)


class Test_FixedIncomeAssets_currentValRendaFixa_ValueErrors:
    """Tests for 'FixedIncomeAssets' class: currentValRendaFixa()."""

    # List of tuples, with the following order per tuple:
    # - inidate, enddate, indexer, rate, buy
    test_currentValRendaFixa_invalid_date_list = [
        # Invalid value for indexer should raise ValueError exceptions
        (date("2000/01/01"), date("2000/01/01"), "A", 1.0, 100),
    ]


class Test_FixedIncomeAssets_currentRendaFixa:
    """Tests for 'FixedIncomeAssets' class: currentRendaFixa()."""

    def test_currentRendaFixa(self):
        """Test the 'FixedIncomeAssets' class: test_currentRendaFixa."""
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
        assets = FixedIncomeAssets()
        title_list = list(assets._getDefaultDataframe())
        df = assets.currentRendaFixa()
        assert isinstance(df, pd.DataFrame) is True
        assert all(item in title_list for item in list(df)) is True
        assert title_list == expected_title_list
