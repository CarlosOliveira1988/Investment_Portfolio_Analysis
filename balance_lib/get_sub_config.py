"""File used to get 'sub' configuration from 'investimentos.ini' file."""

from balance_lib.get_main_config import InvestmentConfig


class SubInvestmentConfig:
    """Class used to get sub configurations related to assets."""

    def __init__(self, main_tag, subtags_list, subtitles_list, config_file):
        """Create the SubInvestmentConfig object.

        The main output of this class is a special dictionary of configuration
        objects, related to the 'InvestmentConfig' class."""
        self.config_main_tag = main_tag
        self.config_subtags_list = subtags_list
        self.config_subtitles_list = subtitles_list
        self.config_file = config_file
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
        subtag_index = self.config_subtags_list.index(subtag)
        return self.config_subtitles_list[subtag_index]

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
                self.config_main_tag,
                config_subtag,
            )
            sub_main_title = self.__getSubConfigMainTitle(config_subtag)
            # The 'sub_subtags' and 'sub_subtitles' at this point represent
            # the tickers, but here we have no idea which are the target ticker
            # list since this information come from extrato spreadsheet
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
