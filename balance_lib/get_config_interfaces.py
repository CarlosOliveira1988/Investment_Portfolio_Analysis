"""File used as interface to get configuration from 'investimentos.ini'."""

import configparser


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
        self.parser = self.__readConfigFile()
        self.target_list = self.__getConfigurations()

    def __readConfigFile(self):
        parser = configparser.ConfigParser()
        if self.config_file:
            parser.read(self.config_file)
        return parser

    def __getUpdatedSubtags(self):
        if self.config_file:
            return self.parser.options(self.main_tag)
        else:
            return []

    def __getConfigurations(self):
        target_list = []
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
                target_list.append(configuration)
        return target_list

    def __checkLists(self, subtags, subtitles, target_list):
        # Look for some failure conditions
        subtags_len = len(subtags)
        subtitles_len = len(subtitles)
        target_len = len(target_list)
        sum_len = subtags_len + subtitles_len + target_len
        if (3 * target_len) != sum_len:
            msg = "All lists must have the same length."
            raise ValueError(msg)

    def __checkStringList(self, string_list):
        def __raiseStringListError():
            msg = "The 'string_list' variable should be a list of strings."
            raise ValueError(msg)

        if isinstance(string_list, list):
            for x in string_list:
                if not isinstance(x, str):
                    __raiseStringListError()
        else:
            __raiseStringListError()

    def __checkNumberList(self, num_list):
        def __raiseNumberListError():
            msg = "The 'num_list' variable should be a list of numbers."
            raise ValueError(msg)

        if isinstance(num_list, list):
            for x in num_list:
                if not ((isinstance(x, int)) or (isinstance(x, float))):
                    __raiseNumberListError()
        else:
            __raiseNumberListError()

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
        self.parser = self.__readConfigFile()
        self.subtags = self.__getUpdatedSubtags()
        self.subtitles = self.subtags.copy()
        self.target_list = self.__getConfigurations()

    def setDynamicValues(self, subtags, subtitles, target_list):
        """Set the main dynamic values (subtags, subtitles, target_list)."""
        # Check for common errors
        self.__checkLists(subtags, subtitles, target_list)
        self.__checkStringList(subtags)
        self.__checkStringList(subtitles)
        self.__checkNumberList(target_list)

        # Copy the new data
        self.subtags = subtags
        self.subtitles = subtitles
        self.target_list = [target * 100 for target in target_list]

        # Update the file with the new data
        self.parser = self.__readConfigFile()
        config_dict = dict(zip(self.subtags, self.target_list))
        self.parser[self.main_tag] = config_dict
        with open(self.config_file, "w") as configfile:
            self.parser.write(configfile)


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
        # Late import due errors related to 'partially initialized module'
        from balance_lib.get_sub_config import SubInvestmentConfig

        self.sub_config = SubInvestmentConfig(
            main_tag,
            subtags,
            subtitles,
            config_file,
        )

    def getSubConfigurationDict(self):
        """Return a dictionary with the configuration objects."""
        return self.sub_config.getConfigurationDict()
