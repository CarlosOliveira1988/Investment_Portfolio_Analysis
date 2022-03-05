"""This file is used to get parameters from 'investimentos.ini' file."""

import configparser
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


class InvestmentConfigManager:
    """Class used to manage configuration file related to investment types."""

    def __init__(self, config_dir):
        """Create the InvestmentConfigManager object."""
        self.config_dir = config_dir
        self.config_file = os.path.join(self.config_dir, "investimentos.ini")
        self.default_config_file = False
        if not self.__configFileExists():
            self.__createDefaultConfigFile()
            self.default_config_file = True

        # Late import due errors related to 'partially initialized module'
        from balance_lib.get_main_config import (
            ClasseDeInvestimento,
            RendaFixa,
            RendaVariavel,
            TesouroDireto,
        )

        self.ClasseDeInvestimento = ClasseDeInvestimento(self.config_file)
        self.RendaVariavel = RendaVariavel(self.config_file)
        self.RendaFixa = RendaFixa(self.config_file)
        self.TesouroDireto = TesouroDireto(self.config_file)

    """Private methods."""

    def __configFileExists(self):
        return os.path.isfile(self.config_file)

    def __createDefaultConfig(self, InvestmentConfigObj, parser):
        invest = InvestmentConfigObj
        main_tag = invest.getMainTag()
        subtags = invest.getSubTagsList()
        config_dict = {}
        # When creating the default configuration file, it is not possible
        # to know which are the assets in the extrato spreadsheet file
        # because here we don't have access to it.
        # Then, 'subtags' is usually an empty list for this case.
        try:
            default_value = float(100 / len(subtags))
        except ZeroDivisionError:
            default_value = 0.0
        for subtag in subtags:
            config_dict[subtag] = default_value
        parser[main_tag] = config_dict

    def __createDefaultSubConfig(self, InvestmentConfigObj, parser):
        # Late import due errors related to 'partially initialized module'
        from balance_lib.get_sub_config import SubInvestmentConfig

        invest = InvestmentConfigObj
        sub_config = SubInvestmentConfig(
            invest.getMainTag(),
            invest.getSubTagsList(),
            invest.getSubTitlesList(),
            invest.getConfigFile(),
        )
        sub_config_dict = sub_config.getConfigurationDict()
        for config in sub_config_dict.values():
            self.__createDefaultConfig(config, parser)

    def __createDefaultConfigFile(self):
        # Late import due errors related to 'partially initialized module'
        from balance_lib.get_main_config import (
            ClasseDeInvestimento,
            RendaFixa,
            RendaVariavel,
            TesouroDireto,
        )

        # ConfigParser
        parser = configparser.ConfigParser()

        # Default configuration: main tags
        default_config_dict = {
            "[ClasseDeInvestimento]": ClasseDeInvestimento(None),
            "[RendaVariavel]": RendaVariavel(None),
            "[RendaFixa]": RendaFixa(None),
            "[TesouroDireto]": TesouroDireto(None),
        }
        for default_config in default_config_dict.values():
            self.__createDefaultConfig(default_config, parser)

        # Default configuration: 2nd level tags
        default_sub_config_dict = {
            "[RV_ACOES]": RendaVariavel(None),
            "[RV_BDR]": RendaVariavel(None),
            "[RV_FII]": RendaVariavel(None),
            "[RV_ETF]": RendaVariavel(None),
            "[RF_PREFIXADO]": RendaFixa(None),
            "[RF_CDI]": RendaFixa(None),
            "[RF_IPCA]": RendaFixa(None),
            "[TD_PREFIXADO]": TesouroDireto(None),
            "[TD_SELIC]": TesouroDireto(None),
            "[TD_IPCA]": TesouroDireto(None),
        }
        for default_sub_config in default_sub_config_dict.values():
            self.__createDefaultSubConfig(default_sub_config, parser)

        # Create the default configuration file
        with open(self.config_file, "w") as configfile:
            parser.write(configfile)

    """Public methods."""

    def getConfigFile(self):
        """Return the string related to the configuration file address."""
        return self.config_file

    def getConfigFileDir(self):
        """Return the string related to the configuration directory address."""
        return self.config_dir

    def isDefaultConfigFile(self):
        """Return if the default configuration file was generated."""
        return self.default_config_file


class ConfigurationManager(InvestmentConfigManager):
    """Class used to handle with configurations."""

    def __init__(self, extrato_path):
        """Create the ConfigurationManager object."""
        super().__init__(extrato_path)
        if self.isDefaultConfigFile():
            self.showDefatultConfigurationMsg()

    """Public methods."""

    def showDefatultConfigurationMsg(self):
        """Show the message related to default configuration file."""
        msg = "Um arquivo de configurações 'investimentos.ini' foi criado "
        msg += "no seguinte diretório:\n\n" + self.getConfigFileDir()
        msg += "\n\nConsidere editar esse arquivo conforme necessário."
        QMessageBox.information(
            QtWidgets.QWidget(),
            "Análise de Portfólio",
            msg,
            QMessageBox.Ok,
        )
