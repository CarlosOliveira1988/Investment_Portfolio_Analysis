"""This file is useful to handle special tab panels portfolio balancing."""

import pandas as pd
from gui_lib.window import Window
from widget_lib.tab_viewer import TabViewerWidget

from balance_lib.balance_treeview import BalancingBoxTreeview
from balance_lib.get_main_config import RendaVariavel


class GeneralDataframes:
    """Class used to manipulate general dataframes."""

    def __init__(self, RendaVariavel_df, RendaFixa_df, TesouroDireto_df):
        """Create the GeneralDataframes object.

        Arguments:
        - RendaVariavel_df, RendaFixa_df, TesouroDireto_df: short and
        filtered dataframes exported by the 'PortfolioInvestment' class
        type, grouped per investment types:
          * RendaVariavel_df: ""Ações", "BDR", "ETF", "FII"
          * RendaFixa_df: "Prefixado", "CDI", "IPCA"
          * TesouroDireto_df: "Prefixado", "SELIC", "IPCA"
        """
        # Main dataframes
        self.RendaVariavel_df = RendaVariavel_df
        self.RendaFixa_df = RendaFixa_df
        self.TesouroDireto_df = TesouroDireto_df
        self.ClasseDeInvestimento_df = self.__getClasseDeInvestimentoDF()

    """Private methods."""

    def __getClasseDeInvestimentoDF(self):
        # Copy and concatenate the main dataframes
        RV_df = self.RendaVariavel_df.copy()
        RF_df = self.RendaFixa_df.copy()
        TD_df = self.TesouroDireto_df.copy()
        CI_df = pd.concat([RV_df, RF_df, TD_df], ignore_index=True, sort=False)

        # Replace some column values
        replace_dict = {}
        for subtitle in RendaVariavel(None).getSubTitlesList():
            replace_dict[subtitle] = "Renda Variável"
        return CI_df.replace(to_replace=replace_dict)

    """Public methods."""

    def getClasseDeInvestimentoDF(self):
        """Return the ClasseDeInvestimento dataframe."""
        return self.ClasseDeInvestimento_df.copy()

    def getRendaVariavelDF(self):
        """Return the RendaVariavel dataframe."""
        return self.RendaVariavel_df.copy()

    def getRendaFixaDF(self):
        """Return the RendaFixa dataframe."""
        return self.RendaFixa_df.copy()

    def getTesouroDiretoDF(self):
        """Return the TesouroDireto dataframe."""
        return self.TesouroDireto_df.copy()


class TabPanelInterface(TabViewerWidget):
    """Class used to create special tabs for balancing portfolio."""

    def __init__(
        self,
        tree_list,
        tab_title,
        border_size=Window.DEFAULT_BORDER_SIZE,
    ):
        """Create the TabPanelInterface object.

        Arguments:
        - tree_list: a list of 'ResizableTreeviewPandas' objects
        - tab_title: a string to be displayed in the tab
        - border_size: a int value to define the border size
          (by default: Window.DEFAULT_BORDER_SIZE)
        """
        super().__init__(tree_list, tab_title, border_size)

    """Public methods."""

    def resize(self):
        """Resize the treeview."""
        for box in self.box_list:
            box.resize()


class GeneralTabPanel(TabPanelInterface):
    """Class used to create the 'Geral' tab."""

    def __init__(
        self,
        RendaVariavel_df,
        RendaFixa_df,
        TesouroDireto_df,
        ConfigurationManagerObj,
    ):
        """Create the GeneralTabPanel object.

        Arguments:
        - RendaVariavel_df, RendaFixa_df, TesouroDireto_df: short and
        filtered dataframes exported by the 'PortfolioInvestment' class
        type, grouped per investment types:
          * RendaVariavel_df: ""Ações", "BDR", "ETF", "FII"
          * RendaFixa_df: "Prefixado", "CDI", "IPCA"
          * TesouroDireto_df: "Prefixado", "SELIC", "IPCA"
        - ConfigurationManagerObj: an object related to the
        'ConfigurationManager' class type
        """
        # Dataframes
        self.GeneralDataframes = GeneralDataframes(
            RendaVariavel_df,
            RendaFixa_df,
            TesouroDireto_df,
        )

        # Investment boxes
        self.config = ConfigurationManagerObj
        self.tree_list = []
        self.box_list = []
        self.sub_config_list = []
        self.ClasseDeInvestimento = self.__createBoxTree(
            self.config.ClasseDeInvestimento,
            self.GeneralDataframes.getClasseDeInvestimentoDF(),
        )
        self.RendaVariavel = self.__createBoxTree(
            self.config.RendaVariavel,
            self.GeneralDataframes.getRendaVariavelDF(),
        )
        self.RendaFixa = self.__createBoxTree(
            self.config.RendaFixa,
            self.GeneralDataframes.getRendaFixaDF(),
        )
        self.TesouroDireto = self.__createBoxTree(
            self.config.TesouroDireto,
            self.GeneralDataframes.getTesouroDiretoDF(),
        )

        # 'Geral' tab widget
        super().__init__(self.tree_list, "Geral")

    """Private methods."""

    def __createBoxTree(self, InvestmentConfigObj, dataframe=None):
        boxtree = BalancingBoxTreeview(
            InvestmentConfigObj,
            dataframe,
            immutable_type_list=True,
        )
        self.tree_list.append(boxtree.getTree())
        self.box_list.append(boxtree)
        self.sub_config_list.append(InvestmentConfigObj)
        return boxtree

    """Public methods."""

    def updateConfigurationValues(self):
        """Update configuration values from configuration file."""
        for index, sub_config in enumerate(self.sub_config_list):
            sub_config.updateDynamicValuesFromFile()
            self.box_list[index].updateConfigurationValues()


class AssetsTabPanel(TabPanelInterface):
    """Class used to create the 'Assets' tabs.

    The 'AssetsTabPanel' is useful to create the special tabs, with several
    treeview objects, related to:
    - Renda Variável
    - Renda Fixa
    - Tesouro Direto
    """

    def __init__(self, assets_df, InvestmentConfigObj, is_default_config):
        """Create the AssetsTabPanel object.

        Arguments:
        - assets_df: the filtered dataframe per investment type (Renda
        Variável, Renda Fixa, Tesouro Direto)
        - InvestmentConfigObj: the configuration object type, related
        to the 'assets_df' variable, that is inherited from the
        'InvestmentConfigInterface' class
        - is_default_config: flag to indicate if the configuration file
        is on its default state or not
        """
        self.assets_df = assets_df
        self.config = InvestmentConfigObj
        self.is_default = is_default_config
        self.__createBalancingBoxTreeview()
        super().__init__(self.tree_list, self.config.getMainTitle())

    """Private methods."""

    def __getMergedSubTags(self, sub_config):
        sub_titles = self.__getMergedSubTitles(sub_config)
        sub_tags = [title.lower() for title in sub_titles]
        return sub_tags

    def __getMergedSubTitles(self, sub_config):
        # From config file/object
        sub_titles = sub_config.getSubTitlesList().copy()
        filter_column = sub_config.getFilterColumn()

        # In this point, dataframe will have unique 'ticker' lines
        df = self.__getFilteredDataframe(sub_config)
        sub_titles_dataframe = df[filter_column].tolist().copy()

        # Return an union of the lists, including the config lists at first
        sub_titles.extend(sub_titles_dataframe)
        return sub_titles

    def __getMergedTargets(self, sub_config, merged_sub_tags):
        # It is expected 'sub_targets' and 'sub_tags' will have the same length
        # because both come from the configuration file.
        #
        # Also, it is expected that the length of 'merged_sub_tags' is equal
        # or greater than the length of 'sub_tags', because it is an union of
        # data from configuration file and data from the extrato spreadsheet
        sub_targets = sub_config.getTargetList()
        sub_tags = sub_config.getSubTagsList()

        # Merge the target list
        target_list = []
        for merged_sub_tag in merged_sub_tags:
            try:
                index = sub_tags.index(merged_sub_tag.lower())
                target_list.append(sub_targets[index])
            except IndexError:
                target_list.append(0.0)
            except ValueError:
                target_list.append(0.0)

        return target_list

    def __removeDuplicates(self, msub_tags, msub_titles, msub_targets):
        sub_tags = []
        sub_titles = []
        sub_targets = []
        # The 'tags' in configuration file is handled as 'lower characters'
        # but in the extrato spreadsheet as case sensitive.
        #
        # Since the configuration data is present at the beggining of the
        # lists, then it is preferable to invert the lists before the 'loop'
        low_mgd_sub_tags = [tag.lower() for tag in msub_tags]
        low_mgd_sub_tags.reverse()
        msub_tags.reverse()
        msub_titles.reverse()
        msub_targets.reverse()
        # Remove the duplicates
        for index, tag in enumerate(low_mgd_sub_tags):
            if tag in sub_tags:
                pass
            else:
                sub_tags.append(msub_tags[index])
                sub_titles.append(msub_titles[index])
                sub_targets.append(msub_targets[index])
        return sub_tags, sub_titles, sub_targets

    def __mergeConfigurations(self, sub_config):
        # Merge configuration that will be used in the BalancingBox object
        sub_config.updateDynamicValuesFromFile()
        mgdsub_tags = self.__getMergedSubTags(sub_config)
        mgdsub_titles = self.__getMergedSubTitles(sub_config)
        mgdsub_targets = self.__getMergedTargets(sub_config, mgdsub_tags)
        mgdsub_tags, mgdsub_titles, mgdsub_targets = self.__removeDuplicates(
            mgdsub_tags, mgdsub_titles, mgdsub_targets
        )
        sub_config.setDynamicValues(
            mgdsub_tags,
            mgdsub_titles,
            mgdsub_targets,
        )

    def __getFilteredDataframe(self, sub_config):
        # Filter the dataframe
        filter_column = self.config.getFilterColumn()
        filter_value = sub_config.getMainTitle()
        df = self.assets_df.copy()
        df = df[df[filter_column] == filter_value]
        return df.reset_index(drop=True)

    def __createBalancingBoxTreeview(self):
        self.tree_list = []
        self.box_list = []
        self.sub_config_list = []
        sub_config_dict = self.config.getSubConfigurationDict()
        for sub_config in sub_config_dict.values():
            # Before creating the BalancingBoxTreeview, we need to merge
            # the configuration lists related to the config file and to the
            # assets dataframe
            self.__mergeConfigurations(sub_config)
            fassets_df = self.__getFilteredDataframe(sub_config)
            balancing_box = BalancingBoxTreeview(sub_config, fassets_df)
            self.tree_list.append(balancing_box.getTree())
            self.box_list.append(balancing_box)
            self.sub_config_list.append(sub_config)

    """Public methods."""

    def updateConfigurationValues(self):
        """Update configuration values from configuration file."""
        for index, sub_config in enumerate(self.sub_config_list):
            self.__mergeConfigurations(sub_config)
            self.box_list[index].updateConfigurationValues()
