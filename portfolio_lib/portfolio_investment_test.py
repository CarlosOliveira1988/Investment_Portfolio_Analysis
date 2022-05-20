"""This file is used to test the 'portfolio_investment.py'."""

import os
import sys

import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from portfolio_lib.portfolio_investment import PortfolioInvestment


class Test_PortfolioInvestment:
    """Tests for 'PortfolioInvestment' class."""

    def test_no_file_initialization(self):
        """Test the 'PortfolioInvestment' initialization."""
        portfolio = PortfolioInvestment()

        # Since 'fileOperations=None', the file is invalid
        assert portfolio.isValidFile() is False
        assert portfolio.getExtratoPath() is None

        # Since 'fileOperations=None', the extrato is the default dataframe
        VIncomeDF = portfolio.currentPortfolio()
        title_list = portfolio.VariableIncome.getColumnsTitleList()
        assert isinstance(VIncomeDF, pd.DataFrame) is True
        assert all(item in title_list for item in list(VIncomeDF)) is True
        assert len(VIncomeDF) == 0

        FIncomeDF = portfolio.currentRendaFixa()
        title_list = portfolio.FixedIncome.getColumnsTitleList()
        assert isinstance(FIncomeDF, pd.DataFrame) is True
        assert all(item in title_list for item in list(FIncomeDF)) is True
        assert len(FIncomeDF) == 0

        TreasuriesDF = portfolio.currentTesouroDireto()
        title_list = portfolio.Treasuries.getColumnsTitleList()
        assert isinstance(TreasuriesDF, pd.DataFrame) is True
        assert all(item in title_list for item in list(TreasuriesDF)) is True
        assert len(TreasuriesDF) == 0

        GDriveDF = portfolio.currentPortfolioGoogleDrive(False, False)
        assert isinstance(GDriveDF, pd.DataFrame) is True
        assert len(TreasuriesDF) == 0

    def test_not_valid_file_initialization(self):
        """Test the 'PortfolioInvestment' initialization."""
        portfolio = PortfolioInvestment("NOT_VALID_FILE")

        # Since 'fileOperations=None', the file is invalid
        assert portfolio.isValidFile() is False
        assert portfolio.getExtratoPath() is None

        # Since 'fileOperations=None', the extrato is the default dataframe
        VIncomeDF = portfolio.currentPortfolio()
        title_list = portfolio.VariableIncome.getColumnsTitleList()
        assert isinstance(VIncomeDF, pd.DataFrame) is True
        assert all(item in title_list for item in list(VIncomeDF)) is True
        assert len(VIncomeDF) == 0

        FIncomeDF = portfolio.currentRendaFixa()
        title_list = portfolio.FixedIncome.getColumnsTitleList()
        assert isinstance(FIncomeDF, pd.DataFrame) is True
        assert all(item in title_list for item in list(FIncomeDF)) is True
        assert len(FIncomeDF) == 0

        TreasuriesDF = portfolio.currentTesouroDireto()
        title_list = portfolio.Treasuries.getColumnsTitleList()
        assert isinstance(TreasuriesDF, pd.DataFrame) is True
        assert all(item in title_list for item in list(TreasuriesDF)) is True
        assert len(TreasuriesDF) == 0

        GDriveDF = portfolio.currentPortfolioGoogleDrive(False, False)
        assert isinstance(GDriveDF, pd.DataFrame) is True
        assert len(TreasuriesDF) == 0

    def test_valid_file_initialization(self):
        """Test the 'PortfolioInvestment' initialization."""
        file = os.path.join(SCRIPT_DIR, "PORTFOLIO_TEMPLATE.xlsx")
        portfolio = PortfolioInvestment(file)

        # Since 'fileOperations=None', the file is invalid
        assert portfolio.isValidFile() is True
        assert isinstance(portfolio.getExtratoPath(), str) is True
        assert portfolio.getExtratoPath() == SCRIPT_DIR

        # Since 'fileOperations=None', the extrato is the default dataframe
        VIncomeDF = portfolio.currentPortfolio()
        title_list = portfolio.VariableIncome.getColumnsTitleList()
        assert isinstance(VIncomeDF, pd.DataFrame) is True
        assert all(item in title_list for item in list(VIncomeDF)) is True
        assert len(VIncomeDF) > 0

        FIncomeDF = portfolio.currentRendaFixa()
        title_list = portfolio.FixedIncome.getColumnsTitleList()
        assert isinstance(FIncomeDF, pd.DataFrame) is True
        assert all(item in title_list for item in list(FIncomeDF)) is True
        assert len(FIncomeDF) > 0

        TreasuriesDF = portfolio.currentTesouroDireto()
        title_list = portfolio.Treasuries.getColumnsTitleList()
        assert isinstance(TreasuriesDF, pd.DataFrame) is True
        assert all(item in title_list for item in list(TreasuriesDF)) is True
        assert len(TreasuriesDF) > 0

        GDriveDF = portfolio.currentPortfolioGoogleDrive(False, False)
        assert isinstance(GDriveDF, pd.DataFrame) is True
        assert len(GDriveDF) > 0
