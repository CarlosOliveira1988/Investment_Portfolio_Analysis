"""This file is used to test the 'get_config.py'."""

import os

import pytest

from get_config import (
    ClasseDeInvestimento,
    InvestmentConfig,
    InvestmentConfigManager,
    RendaFixa,
    RendaVariavel,
    SubInvestmentConfig,
    TesouroDireto,
)


class Test_InvestmentConfigManager:
    """Tests for 'InvestmentConfigManager' class."""

    @classmethod
    def setup_class(cls):
        """Start-up the test class."""
        cls.config_manager = InvestmentConfigManager(os.path.curdir)
        cls.file = cls.config_manager.getConfigFile()

    @classmethod
    def teardown_class(cls):
        """End-up the test class."""
        os.remove(cls.file)

    def test_ClasseDeInvestimento_tag(self):
        """Test the 'ClasseDeInvestimento' tag."""
        file = Test_InvestmentConfigManager.file
        main_tag = "ClasseDeInvestimento"
        title = "Classe de Investimento"
        subtag_list = ["RendaVariavel", "RendaFixa", "TesouroDireto"]
        subtitle_list = ["Renda Variável", "Renda Fixa", "Tesouro Direto"]
        target_list = [100 / len(subtag_list)] * len(subtag_list)
        target_list = [x / 100.0 for x in target_list]
        cfg = ClasseDeInvestimento(file)
        assert cfg.getMainTag() == main_tag
        assert cfg.getSubTagsList() == subtag_list
        assert cfg.getSubTitlesList() == subtitle_list
        assert cfg.getMainTitle() == title
        assert cfg.getTargetList()[0] == pytest.approx(target_list[0], 0.001)

    def test_RendaVariavel_tag(self):
        """Test the 'RendaVariavel' tag."""
        file = Test_InvestmentConfigManager.file
        main_tag = "RendaVariavel"
        title = "Renda Variável"
        subtag_list = ["Acoes", "BDR", "FII", "ETF"]
        subtitle_list = ["Ações", "BDR", "FII", "ETF"]
        target_list = [100 / len(subtag_list)] * len(subtag_list)
        target_list = [x / 100.0 for x in target_list]
        cfg = RendaVariavel(file)
        assert cfg.getMainTag() == main_tag
        assert cfg.getSubTagsList() == subtag_list
        assert cfg.getSubTitlesList() == subtitle_list
        assert cfg.getMainTitle() == title
        assert cfg.getTargetList()[0] == pytest.approx(target_list[0], 0.001)

    def test_RendaFixa_tag(self):
        """Test the 'RendaFixa' tag."""
        file = Test_InvestmentConfigManager.file
        main_tag = "RendaFixa"
        title = "Renda Fixa"
        subtag_list = ["PREFIXADO", "CDI", "IPCA"]
        subtitle_list = ["PREFIXADO", "CDI", "IPCA"]
        target_list = [100 / len(subtag_list)] * len(subtag_list)
        target_list = [x / 100.0 for x in target_list]
        cfg = RendaFixa(file)
        assert cfg.getMainTag() == main_tag
        assert cfg.getSubTagsList() == subtag_list
        assert cfg.getSubTitlesList() == subtitle_list
        assert cfg.getMainTitle() == title
        assert cfg.getTargetList()[0] == pytest.approx(target_list[0], 0.001)

    def test_TesouroDireto_tag(self):
        """Test the 'TesouroDireto' tag."""
        file = Test_InvestmentConfigManager.file
        main_tag = "TesouroDireto"
        title = "Tesouro Direto"
        subtag_list = ["PREFIXADO", "SELIC", "IPCA"]
        subtitle_list = ["PREFIXADO", "SELIC", "IPCA"]
        target_list = [100 / len(subtag_list)] * len(subtag_list)
        target_list = [x / 100.0 for x in target_list]
        cfg = TesouroDireto(file)
        assert cfg.getMainTag() == main_tag
        assert cfg.getSubTagsList() == subtag_list
        assert cfg.getSubTitlesList() == subtitle_list
        assert cfg.getMainTitle() == title
        assert cfg.getTargetList()[0] == pytest.approx(target_list[0], 0.001)

    def test_SubInvestmentConfig(self):
        """Test the 'SubInvestmentConfig' class."""
        file = Test_InvestmentConfigManager.file
        cfg = RendaVariavel(file)
        sub_cfg = SubInvestmentConfig(cfg)
        sub_cfg_dict = sub_cfg.getConfigurationDict()
        sub_cfg_dict_list = list(sub_cfg_dict)
        expected_dict_list = ["RV_ACOES", "RV_BDR", "RV_FII", "RV_ETF"]
        for sub_tag in expected_dict_list:
            assert isinstance(sub_cfg_dict[sub_tag], InvestmentConfig) is True
        assert sub_cfg_dict_list.sort() == expected_dict_list.sort()
