"""This file is used to test the 'extrato_manager.py'."""

import os
import sys

import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from portfolio_lib.extrato_manager import ExtratoFileManager


class Test_ExtratoFileManager:
    """Tests for 'ExtratoFileManager' class."""

    def test_no_file_initialization(self):
        """Test the 'ExtratoFileManager' initialization."""
        manager = ExtratoFileManager()
        # Since 'fileOperations=None', the file is invalid
        assert manager.isValidFile() is False
        assert manager.getExtratoPath() is None
        # Since 'fileOperations=None', the extrato is the default dataframe
        dataframe = manager.getExtrato()
        assert isinstance(dataframe, pd.DataFrame) is True
        title_list = list(dataframe)
        get_title_list = manager.getExpectedColumnsTitleList()
        assert all(item in title_list for item in get_title_list) is True
        assert title_list == get_title_list
        assert len(dataframe) == 0

    def test_not_valid_file_initialization(self):
        """Test the 'ExtratoFileManager' initialization."""
        manager = ExtratoFileManager("NOT_VALID_FILE")
        # Since 'fileOperations=None', the file is invalid
        assert manager.isValidFile() is False
        assert manager.getExtratoPath() is None
        # Since 'fileOperations=None', the extrato is the default dataframe
        dataframe = manager.getExtrato()
        assert isinstance(dataframe, pd.DataFrame) is True
        title_list = list(dataframe)
        get_title_list = manager.getExpectedColumnsTitleList()
        assert all(item in title_list for item in get_title_list) is True
        assert title_list == get_title_list
        assert len(dataframe) == 0

    def test_valid_file_initialization(self):
        """Test the 'ExtratoFileManager' initialization."""
        file = os.path.join(SCRIPT_DIR, "PORTFOLIO_TEMPLATE.xlsx")
        manager = ExtratoFileManager(file)
        # Since 'fileOperations=someValidFile', the file is valid
        assert manager.isValidFile() is True
        assert isinstance(manager.getExtratoPath(), str) is True
        assert manager.getExtratoPath() == SCRIPT_DIR
        # Since 'fileOperations=someValidFile', the extrato is a dataframe
        dataframe = manager.getExtrato()
        assert isinstance(dataframe, pd.DataFrame) is True
        title_list = list(dataframe)
        get_title_list = manager.getExpectedColumnsTitleList()
        assert all(item in title_list for item in get_title_list) is True
        assert title_list == get_title_list
        assert len(dataframe) > 0
