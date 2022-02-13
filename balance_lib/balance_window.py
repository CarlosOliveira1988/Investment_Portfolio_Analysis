"""This file has classes to show windows for portfolio balancing purpose."""

import pandas as pd
from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from widget_lib.tab_viewer import TabViewerWidget

from balance_lib.balance import BalancingBox
from balance_lib.get_config import (
    InvestmentConfigManager,
    RendaVariavel,
    SubInvestmentConfig,
)


class BalancingBoxTreeview:
    """Class used to create special treeview related to BalancingBox."""

    def __init__(self, InvestmentConfigObject, dataframe):
        """Create the BalancingBoxTreeview object."""
        self.investment = InvestmentConfigObject

        # BalancingBox
        filter_column = self.investment.getFilterColumn()
        target_list = self.investment.getTargetList()
        type_list = self.investment.getSubTitlesList()
        value_list = self.__getValueList(type_list, dataframe, filter_column)
        self.box = BalancingBox(self.investment.getMainTitle())
        self.box.setValues(target_list, value_list, type_list)

        # Treeview
        self.tree = ResizableTreeviewPandas(
            self.box.getFormattedDataframe(),
            split_big_title=False,
        )
        self.tree.showPandas()
        self.resize()

    """Private methods."""

    def __getValueList(self, type_list, dataframe, filter_column):
        value_list = []
        for invest_type in type_list:
            df = dataframe[dataframe[filter_column] == invest_type]
            value = df["Preço mercado"].sum()
            value_list.append(value)
        return value_list

    """Public methods."""

    def getTree(self):
        """Return the Tree object."""
        return self.tree

    def resize(self):
        """Resize the treeview."""
        self.tree.resizeColumnsToTreeViewWidth()


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
        self.sub_config = SubInvestmentConfig(self.config)
        self.box_list = []
        self.tree_list = self.__getBalancingBoxTreeviewList()
        super().__init__(
            self.tree_list,
            self.config.getMainTitle(),
            Window.DEFAULT_BORDER_SIZE,
        )

    """Private methods."""

    def __getBalancingBoxTreeviewList(self):
        tree_list = []
        sub_config_dict = self.sub_config.getConfigurationDict()
        for sub_config in sub_config_dict.values():
            box = BalancingBoxTreeview(sub_config, self.assets_df)
            tree_list.append(box.getTree())
            self.box_list.append(box)
        return tree_list

    """Public methods."""

    def resize(self):
        """Resize the treeview."""
        for box in self.box_list:
            box.resize()


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


class BalancingWindowTabs(QtWidgets.QTabWidget):
    """Class used to create special tabs."""

    def __init__(
        self,
        RendaVariavel_df,
        RendaFixa_df,
        TesouroDireto_df,
        ConfigurationManagerObj,
    ):
        """Create the BalancingWindowTabs object."""
        super().__init__()

        # Control variable
        self.tab_list = []

        # General tab
        self.GeneralTabPanel = self.__addGeneralTab(
            RendaVariavel_df,
            RendaFixa_df,
            TesouroDireto_df,
            ConfigurationManagerObj,
        )

        # Assets tabs
        self.RendaVariavelTabPanel = self.__addAssetsTab(
            RendaVariavel_df,
            ConfigurationManagerObj.RendaVariavel,
        )
        self.RendaFixaTabPanel = self.__addAssetsTab(
            RendaFixa_df,
            ConfigurationManagerObj.RendaFixa,
        )
        self.TesouroDiretoTabPanel = self.__addAssetsTab(
            TesouroDireto_df,
            ConfigurationManagerObj.TesouroDireto,
        )

        # Connect tab event
        self.currentChanged.connect(self.onChange)

    """Private methods."""

    def __getTabPanelAndIndex(self, tab_panel):
        tab_index = self.addTab(tab_panel.getTab(), tab_panel.getTabTitle())
        self.tab_list.append(tab_panel)
        return tab_panel, tab_index

    def __addGeneralTab(
        self,
        RendaVariavel_df,
        RendaFixa_df,
        TesouroDireto_df,
        InvestmentConfigObj,
    ):
        tab_panel = GeneralTabPanel(
            RendaVariavel_df,
            RendaFixa_df,
            TesouroDireto_df,
            InvestmentConfigObj,
        )
        return self.__getTabPanelAndIndex(tab_panel)

    def __addAssetsTab(self, assets_df, InvestmentConfigObj):
        tab_panel = AssetsTabPanel(assets_df, InvestmentConfigObj)
        return self.__getTabPanelAndIndex(tab_panel)

    """Public methods."""

    def onChange(self, index):
        """Onchange tab method to render the table columns."""
        for tab in self.tab_list:
            # if index == tab.getTabIndex():
            tab.resize()


class BalancingWindow(QtWidgets.QWidget):
    """Window class used to show Balancing Portfolio frames."""

    def __init__(
        self,
        RendaVariavel_df,
        RendaFixa_df,
        TesouroDireto_df,
        extrato_path,
        auto_show=True,
    ):
        """Create the BalancingWindow object.

        Arguments:
        - RendaVariavel_df, RendaFixa_df, TesouroDireto_df: dataframes related
        to the opened positions in the portfolio
        - auto_show (True/False): flag to show window while creating the object
        """
        super().__init__()

        # Configuration manager
        self.config = ConfigurationManager(extrato_path)

        # Tab group
        self.TabGroup = BalancingWindowTabs(
            RendaVariavel_df,
            RendaFixa_df,
            TesouroDireto_df,
            self.config,
        )

        # Set the window properties
        self.__setWindowProperties()

        # Show the window
        if auto_show:
            self.showMaximized()

    """Private methods."""

    def __setWindowProperties(self):
        spacing = Window.DEFAULT_BORDER_SIZE / 2
        internal_spacing = Window.DEFAULT_BORDER_SIZE

        # Create the grid object
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid.setSpacing(internal_spacing)
        self.grid.addWidget(self.TabGroup)

        # Set the grid layout
        self.setLayout(self.grid)

        # Set the title
        self.setWindowTitle("Balanceamento de Carteira")
