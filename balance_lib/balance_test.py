"""This file is used to test the 'balance.py'."""

import pandas as pd
import pytest

from balance import ContributionBox, InvestmentBox


class Test_InvestmentBox:
    """Tests for 'InvestmentBox' class."""

    def test_getDataframe(self):
        """Test the 'getDataframe' method."""
        box = InvestmentBox("Classe de investimento")
        boxdf = box.getDataframe()

        # A dataframe with 1 total line is expected
        assert isinstance(boxdf, pd.DataFrame) is True
        assert len(boxdf) == 1

        # The total line has values=0
        assert boxdf["Meta(R$)"].sum() == 0.0
        assert boxdf["Atual(R$)"].sum() == 0.0
        assert boxdf["Meta(%)"].sum() == 0.0
        assert boxdf["Atual(%)"].sum() == 0.0

    def test_setValues(self):
        """Test the 'setValues' method."""
        box = InvestmentBox("Classe de investimento")
        type_list = ["Renda Variável", "Renda Fixa", "Tesouro Direto"]
        value_list = [10000, 16000, 100000]  # total=126.000
        target_list = [0.08, 0.12, 0.80]  # total=1.00 or 100%
        box.setValues(target_list, value_list, type_list)
        boxdf = box.getDataframe()

        # A dataframe with 3 data lines + 1 total line is expected: 4 lines
        assert isinstance(boxdf, pd.DataFrame) is True
        assert len(boxdf) == 4
        assert box.getTotalValue() == 126000

        # The bellow asserts are "2x" due the total line
        assert boxdf["Meta(R$)"].sum() == 2 * 126000
        assert boxdf["Atual(R$)"].sum() == 2 * 126000
        assert boxdf["Meta(%)"].sum() == pytest.approx(2 * 1.0, 0.001)
        assert boxdf["Atual(%)"].sum() == pytest.approx(2 * 1.0, 0.001)


class Test_ContributionBox:
    """Tests for 'ContributionBox' class."""

    def test_getDataframe(self):
        """Test the 'getDataframe' method."""
        cbox = ContributionBox("Classe de investimento")
        boxdf = cbox.getDataframe()

        # A dataframe with 1 total line is expected
        assert isinstance(boxdf, pd.DataFrame) is True
        assert len(boxdf) == 1

        # The total line has values=0
        assert boxdf["Meta(R$)"].sum() == 0.0
        assert boxdf["Atual(R$)"].sum() == 0.0
        assert boxdf["Meta(%)"].sum() == 0.0
        assert boxdf["Atual(%)"].sum() == 0.0

    def test_setValues(self):
        """Test the 'setValues' method."""
        cbox = ContributionBox("Classe de investimento")
        type_list = ["Renda Variável", "Renda Fixa", "Tesouro Direto"]
        value_list = [10000, 16000, 100000]  # total=126.000
        target_list = [0.08, 0.12, 0.80]  # total=1.00 or 100%
        cbox.setValues(target_list, value_list, type_list)
        boxdf = cbox.getDataframe()

        # A dataframe with 3 data lines + 1 total line is expected: 4 lines
        assert isinstance(boxdf, pd.DataFrame) is True
        assert len(boxdf) == 4
        assert cbox.getTotalPlusContribution() == 126000

        # The bellow asserts are "2x" due the total line
        assert boxdf["Meta(R$)"].sum() == 2 * 126000
        assert boxdf["Atual(R$)"].sum() == 2 * 126000
        assert boxdf["Meta(%)"].sum() == pytest.approx(2 * 1.0, 0.001)
        assert boxdf["Atual(%)"].sum() == pytest.approx(2 * 1.0, 0.001)
