"""This file is useful to handle special tab panels portfolio balancing."""

import pandas as pd
from gui_lib.window import Window
from widget_lib.tab_viewer import TabViewerWidget

from balance_lib.balance_treeview import BalancingBoxTreeview
from balance_lib.get_config import RendaVariavel


class GeneralDataframes:
    """Class used to manipulate general dataframes."""

    def __init__(self, RendaVariavel_df, RendaFixa_df, TesouroDireto_df):
        """Create the GeneralDataframes object."""
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
        return CI_df.replace(to_replace=replace_dict, value=None)

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


class GeneralTabPanel(TabViewerWidget):
    """Class used to create the 'Geral' tab."""

    def __init__(
        self,
        RendaVariavel_df,
        RendaFixa_df,
        TesouroDireto_df,
        ConfigurationManagerObj,
    ):
        """Create the GeneralTabPanel object."""
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
        super().__init__(self.tree_list, "Geral", Window.DEFAULT_BORDER_SIZE)

    """Private methods."""

    def __createBoxTree(self, InvestmentConfigObj, dataframe=None):
        boxtree = BalancingBoxTreeview(InvestmentConfigObj, dataframe)
        self.tree_list.append(boxtree.getTree())
        self.box_list.append(boxtree)
        return boxtree

    """Public methods."""

    def resize(self):
        """Resize the treeview."""
        for box in self.box_list:
            box.resize()


class AssetsTabPanel(TabViewerWidget):
    """Class used to create the 'Assets' tabs.

    The 'AssetsTabPanel' is useful to create the special tabs, with several
    treeview objects as follows:
    - Renda Variável
    - Renda Fixa
    - Tesouro Direto
    """

    def __init__(self, assets_df, InvestmentConfigObj):
        """Create the AssetsTabPanel object.

        Arguments:
        - assets_df: the filtered dataframe per investment type (Renda
        Variável, Renda Fixa, Tesouro Direto)
        - InvestmentConfigObj: the InvestmentConfig object type, related
        to the 'assets_df' variable.
        """
        self.assets_df = assets_df
        self.config = InvestmentConfigObj
        self.balancing_box_list = []
        self.treeview_list = []
        self.__createBalancingBoxTreeview()
        super().__init__(
            self.treeview_list,
            self.config.getMainTitle(),
            Window.DEFAULT_BORDER_SIZE,
        )

    """Private methods."""

    def __getMergedSubTags(self, sub_config):
        # From config file/object
        sub_tags = sub_config.getSubTagsList()
        filter_column = sub_config.getFilterColumn()

        # In this point, dataframe will have unique 'ticker' lines
        df = self.assets_df.copy()
        sub_tags_dataframe = df[filter_column].tolist()

        sub_tags.extend(sub_tags_dataframe)
        return sub_tags

    def __getMergedTargets(self, sub_config, merged_sub_tags):
        # From config file/object
        # It is expected 'sub_targets' and 'sub_tags' will have the same length
        sub_targets = sub_config.getTargetList()
        sub_tags = sub_config.getSubTagsList()

        # Merge the target list
        target_list = []
        for merged_sub_tag in merged_sub_tags:
            index = sub_tags.index(merged_sub_tag)
            try:
                target_list.append(sub_targets[index])
            except IndexError:
                target_list.append(0.0)

        return target_list

    def __mergeConfigurations(self, sub_config):
        # Merge configuration that will be used in the BalancingBox object
        mgd_sub_tags = self.__getMergedSubTags(sub_config)
        mgd_sub_titles = mgd_sub_tags.copy()
        mgd_sub_targets = self.__getMergedTargets(sub_config, mgd_sub_tags)
        sub_config.setDynamicValues(
            mgd_sub_tags,
            mgd_sub_titles,
            mgd_sub_targets,
        )
        return sub_config

    def __getFilteredDataframe(self, sub_config):
        # Filter the dataframe
        filter_column = self.config.getFilterColumn()
        filter_value = sub_config.getMainTitle()
        df = self.assets_df.copy()
        df = df[df[filter_column] == filter_value]
        return df.reset_index(drop=True)

    def __createBalancingBoxTreeview(self):
        sub_config_dict = self.config.getSubConfigurationDict()
        for sub_config in sub_config_dict.values():
            # Before creating the BalancingBoxTreeview, we need to merge
            # the configuration lists related to the config file and to the
            # assets dataframe
            sub_config = self.__mergeConfigurations(sub_config)
            fassets_df = self.__getFilteredDataframe(sub_config)
            balancing_box = BalancingBoxTreeview(sub_config, fassets_df)
            self.treeview_list.append(balancing_box.getTree())
            self.balancing_box_list.append(balancing_box)

    """Public methods."""

    def resize(self):
        """Resize the treeview."""
        for box in self.balancing_box_list:
            box.resize()
