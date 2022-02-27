"""This file is used to get parameters from 'investimentos.ini' file."""

import configparser
import os

from PyQt5.QtWidgets import QMessageBox


class InvestmentConfig:
    """Class used to get configurations related to investment types."""

    def __init__(
        self,
        main_tag,
        main_title,
        subtags,
        subtitles,
        filter_column,
        config_file,
    ):
        """Create the InvestmentConfig object.

        Given some special strings (main_tag, main_title, subtags, subtitles,
        filter_column), we may get the 'percentage target' per investment
        type.

        The main output of this class is the 'self.target_list' variable.
        """
        self.main_tag = main_tag
        self.main_title = main_title
        self.subtags = subtags
        self.subtitles = subtitles
        self.filter_column = filter_column
        self.config_file = config_file
        self.parser = configparser.ConfigParser()
        self.__readConfigFile()
        self.__getConfigurations()

    def __readConfigFile(self):
        if self.config_file:
            self.parser.read(self.config_file)

    def __getUpdatedSubtags(self):
        if self.config_file:
            return self.parser.options(self.main_tag)
        else:
            return []

    def __getConfigurations(self):
        self.target_list = []
        if self.config_file:
            for subtag in self.subtags:
                try:
                    configuration = self.parser.getfloat(self.main_tag, subtag)
                    configuration /= 100.0
                except ValueError:
                    configuration = 0.0
                except configparser.NoOptionError:
                    configuration = 0.0
                except configparser.NoSectionError:
                    configuration = 0.0
                self.target_list.append(configuration)

    """Public methods."""

    def getMainTag(self):
        """Return the main tag."""
        return self.main_tag

    def getMainTitle(self):
        """Return the main title."""
        return self.main_title

    def getSubTagsList(self):
        """Return the sub tags list."""
        return self.subtags

    def getSubTitlesList(self):
        """Return the sub titles list."""
        return self.subtitles

    def getTargetList(self):
        """Return the target list."""
        return self.target_list

    def getFilterColumn(self):
        """Return the column name related to the sub titles/tags."""
        return self.filter_column

    def getConfigFile(self):
        """Return the string related to the configuration file address."""
        return self.config_file

    def updateDynamicValuesFromFile(self):
        """Set the main dynamic values (subtags, subtitles, target_list).

        Read the configuration file again and update the related variables.
        """
        self.__readConfigFile()
        self.subtags = self.__getUpdatedSubtags()
        self.subtitles = self.subtags.copy()
        self.__getConfigurations()

    def setDynamicValues(self, subtags, subtitles, target_list):
        """Set the main dynamic values (subtags, subtitles, target_list)."""
        self.subtags = subtags
        self.subtitles = subtitles
        self.target_list = target_list


class SubInvestmentConfig:
    """Class used to get configurations related to assets."""

    def __init__(self, InvestmentConfigObj):
        """Create the SubInvestmentConfig object.

        Arguments:
        - InvestmentConfigObj: any object inherited from 'InvestmentConfig'
        """
        self.config = InvestmentConfigObj
        self.config_subtags_list = self.config.getSubTagsList()
        self.config_file = self.config.getConfigFile()
        self.sub_config_dict = self.__getSubConfigDict()

    """Private methods."""

    def __getSubConfigMainTag(self, maintag, subtag):
        # Example:
        # main_title = "RendaVariavel"
        # subtitle = "ACOES"
        #
        # Result: "RV_ACOES"
        main_tag_dict = {
            "RendaVariavel": "RV_",
            "RendaFixa": "RF_",
            "TesouroDireto": "TD_",
        }
        return main_tag_dict[maintag] + str(subtag).upper()

    def __getSubConfigMainTitle(self, subtag):
        # Example:
        # subtag = "ACOES"
        #
        # Result: "Ações"
        subtags_list = self.config.getSubTagsList()
        subtitles_list = self.config.getSubTitlesList()
        subtag_index = subtags_list.index(subtag)
        return subtitles_list[subtag_index]

    def __getSubConfigDict(self):
        # Example: if we are working with 'RendaVariavel' configuration object,
        # then we will have the following dictionary keys:
        #
        # sub_config_dict["RV_ACOES"]
        # sub_config_dict["RV_BDR"]
        # sub_config_dict["RV_FII"]
        # sub_config_dict["RV_ETF"]
        sub_config_dict = {}
        for config_subtag in self.config_subtags_list:
            sub_main_tag = self.__getSubConfigMainTag(
                self.config.getMainTag(),
                config_subtag,
            )
            sub_main_title = self.__getSubConfigMainTitle(config_subtag)
            sub_subtags = []
            sub_subtitles = []
            sub_config = InvestmentConfig(
                sub_main_tag,
                sub_main_title,
                sub_subtags,
                sub_subtitles,
                "Ticker",
                self.config_file,
            )
            sub_config.updateDynamicValuesFromFile()
            sub_config_dict[sub_main_tag] = sub_config
        return sub_config_dict

    """Public methods."""

    def getConfigurationDict(self):
        """Return a dictionary with the configuration objects.

        See the '__getSubConfigDict()' for more information.
        """
        return self.sub_config_dict.copy()


class ClasseDeInvestimento(InvestmentConfig):
    """Handle the 'ClasseDeInvestimento' tag in configuration file."""

    def __init__(self, config_file):
        """Create the ClasseDeInvestimento object."""
        super().__init__(
            "ClasseDeInvestimento",
            "Classe de Investimento",
            ["RendaVariavel", "RendaFixa", "TesouroDireto"],
            ["Renda Variável", "Renda Fixa", "Tesouro Direto"],
            "Mercado",
            config_file,
        )


class InvestmentConfigInterface(InvestmentConfig):
    """Handle the investment type tags in configuration file."""

    def __init__(
        self,
        main_tag,
        main_title,
        subtags,
        subtitles,
        filter_column,
        config_file,
    ):
        """Create the InvestmentConfigInterface object."""
        super().__init__(
            main_tag,
            main_title,
            subtags,
            subtitles,
            filter_column,
            config_file,
        )
        self.sub_config = SubInvestmentConfig(self)

    def getSubConfigurationDict(self):
        """Return a dictionary with the configuration objects."""
        return self.sub_config.getConfigurationDict()


class RendaVariavel(InvestmentConfigInterface):
    """Handle the 'RendaVariavel' tag in configuration file."""

    def __init__(self, config_file):
        """Create the RendaVariavel object."""
        super().__init__(
            "RendaVariavel",
            "Renda Variável",
            ["Acoes", "BDR", "FII", "ETF"],
            ["Ações", "BDR", "FII", "ETF"],
            "Mercado",
            config_file,
        )


class RendaFixa(InvestmentConfigInterface):
    """Handle the 'RendaFixa' tag in configuration file."""

    def __init__(self, config_file):
        """Create the RendaFixa object."""
        super().__init__(
            "RendaFixa",
            "Renda Fixa",
            ["PREFIXADO", "CDI", "IPCA"],
            ["PREFIXADO", "CDI", "IPCA"],
            "Indexador",
            config_file,
        )


class TesouroDireto(InvestmentConfigInterface):
    """Handle the 'TesouroDireto' tag in configuration file."""

    def __init__(self, config_file):
        """Create the TesouroDireto object."""
        super().__init__(
            "TesouroDireto",
            "Tesouro Direto",
            ["PREFIXADO", "SELIC", "IPCA"],
            ["PREFIXADO", "SELIC", "IPCA"],
            "Indexador",
            config_file,
        )


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
        invest = InvestmentConfigObj
        sub_config = SubInvestmentConfig(invest)
        sub_config_dict = sub_config.getConfigurationDict()
        for config in sub_config_dict.values():
            self.__createDefaultConfig(config, parser)

    def __createDefaultConfigFile(self):
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
            self,
            "Análise de Portfólio",
            msg,
            QMessageBox.Ok,
        )
