"""This file is used to get parameters from 'investimentos.ini' file."""

import configparser
import os


class InvestmentConfig:
    """Class used to get configurations related to investment types."""

    def __init__(
        self, main_tag, main_title, subtags, subtitles, filter_column, config_file
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

    def getSubTagList(self):
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


class ClasseDeInvestimento(InvestmentConfig):
    """Handle the 'ClasseDeInvestimento' tag in configuration file."""

    def __init__(self, config_file):
        """Create the ClasseDeInvestimento object."""
        main_tag = "ClasseDeInvestimento"
        main_title = "Classe de Investimento"
        subtags = ["RendaVariavel", "RendaFixa", "TesouroDireto"]
        subtitles = ["Renda Variável", "Renda Fixa", "Tesouro Direto"]
        filter_column = "Mercado"
        super().__init__(
            main_tag,
            main_title,
            subtags,
            subtitles,
            filter_column,
            config_file,
        )


class RendaVariavel(InvestmentConfig):
    """Handle the 'RendaVariavel' tag in configuration file."""

    def __init__(self, config_file):
        """Create the RendaVariavel object."""
        main_tag = "RendaVariavel"
        main_title = "Renda Variável"
        subtags = ["Acoes", "BDR", "FII", "ETF"]
        subtitles = ["Ações", "BDR", "FII", "ETF"]
        filter_column = "Mercado"
        super().__init__(
            main_tag,
            main_title,
            subtags,
            subtitles,
            filter_column,
            config_file,
        )


class RendaFixa(InvestmentConfig):
    """Handle the 'RendaFixa' tag in configuration file."""

    def __init__(self, config_file):
        """Create the RendaFixa object."""
        main_tag = "RendaFixa"
        main_title = "Renda Fixa"
        subtags = ["PREFIXADO", "CDI", "IPCA"]
        subtitles = ["PREFIXADO", "CDI", "IPCA"]
        filter_column = "Indexador"
        super().__init__(
            main_tag,
            main_title,
            subtags,
            subtitles,
            filter_column,
            config_file,
        )


class TesouroDireto(InvestmentConfig):
    """Handle the 'TesouroDireto' tag in configuration file."""

    def __init__(self, config_file):
        """Create the TesouroDireto object."""
        main_tag = "TesouroDireto"
        main_title = "Tesouro Direto"
        subtags = ["PREFIXADO", "SELIC", "IPCA"]
        subtitles = ["PREFIXADO", "SELIC", "IPCA"]
        filter_column = "Indexador"
        super().__init__(
            main_tag,
            main_title,
            subtags,
            subtitles,
            filter_column,
            config_file,
        )


class InvestmentConfigManager:
    """Class used to manage configuration file related to investment types."""

    def __init__(self, config_dir):
        """Create the InvestmentConfigManager object."""
        self.config_dir = config_dir
        self.config_file = os.path.join(self.config_dir, "investimentos.ini")
        self.default_config_file = False
        if self.__configFileExists():
            pass
        else:
            self.__createDefaultConfigFile()
            self.default_config_file = True

    def __configFileExists(self):
        return os.path.isfile(self.config_file)

    def __createDefaultConfig(self, InvestmentConfig_class, parser):
        invest = InvestmentConfig_class(None)
        main_tag = invest.getMainTag()
        subtags = invest.getSubTagList()
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

    def isDefaultConfigFile(self):
        """Return if the default configuration file was generated."""
        return self.default_config_file
