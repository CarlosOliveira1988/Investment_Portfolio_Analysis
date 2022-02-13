"""This file is used to get parameters from 'investimentos.ini' file."""

import configparser
import os


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
        """Create the InvestmentConfig object."""
        self.main_tag = main_tag
        self.main_title = main_title
        self.subtags = subtags
        self.subtitles = subtitles
        self.filter_column = filter_column
        self.config_file = config_file
        self.parser = configparser.ConfigParser()
        if config_file:
            self.__readConfigFile()
            self.__getConfigurations()

    def __readConfigFile(self):
        self.parser.read(self.config_file)

    def __getConfigurations(self):
        self.target_list = []
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


class RendaVariavel(InvestmentConfig):
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


class RendaFixa(InvestmentConfig):
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


class TesouroDireto(InvestmentConfig):
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

    def __configFileExists(self):
        return os.path.isfile(self.config_file)

    def __createDefaultConfig(self, InvestmentConfig_class, parser):
        invest = InvestmentConfig_class(None)
        main_tag = invest.getMainTag()
        subtags = invest.getSubTagsList()
        config_dict = {}
        default_value = float(100 / len(subtags))
        for subtag in subtags:
            config_dict[subtag] = default_value
        parser[main_tag] = config_dict

    def __createDefaultConfigFile(self):
        # ConfigParser
        parser = configparser.ConfigParser()

        # [ClasseDeInvestimento]
        self.__createDefaultConfig(ClasseDeInvestimento, parser)

        # [RendaVariavel]
        self.__createDefaultConfig(RendaVariavel, parser)

        # [RendaFixa]
        self.__createDefaultConfig(RendaFixa, parser)

        # [TesouroDireto]
        self.__createDefaultConfig(TesouroDireto, parser)

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
