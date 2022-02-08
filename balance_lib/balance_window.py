"""This file has classes to show windows for portfolio balancing purpose."""

import pandas as pd
from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from balance_lib.balance import BalancingBox
from balance_lib.get_config import (
    ClasseDeInvestimento,
    InvestmentConfigManager,
    RendaFixa,
    RendaVariavel,
    TesouroDireto,
)


class BalancingBoxTreeview:
    """Class used to create special treeview related to BalancingBox."""

    def __init__(self, config_file, InvestmentConfigClass, dataframe):
        """Create the BalancingBoxTreeview object."""
        self.investment = InvestmentConfigClass(config_file)

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
        replace_dict = {
            "Ações": "Renda Variável",
            "BDR": "Renda Variável",
            "FII": "Renda Variável",
            "ETF": "Renda Variável",
        }
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


class TabWidget:
    """Class used to show general tabs."""

    def __init__(self, tab_title, special_widget_list):
        """Create the TabWidget object."""
        self.tab_title = tab_title
        self.tab = QtWidgets.QWidget()
        self.grid_tab = QtWidgets.QGridLayout()
        self.grid_tab.setContentsMargins(
            Window.DEFAULT_BORDER_SIZE,
            Window.DEFAULT_BORDER_SIZE,
            Window.DEFAULT_BORDER_SIZE,
            Window.DEFAULT_BORDER_SIZE,
        )
        self.grid_tab.setSpacing(Window.DEFAULT_BORDER_SIZE)
        for special_widget in special_widget_list:
            self.grid_tab.addWidget(special_widget)
        self.tab.setLayout(self.grid_tab)

    """Public methods."""

    def getTab(self):
        """Return the 'Tab' object."""
        return self.tab

    def getGridTab(self):
        """Return the 'GridTab' object."""
        return self.grid_tab

    def getTabTitle(self):
        """Return the 'Tab' title."""
        return self.tab_title

    def setTabIndex(self, tab_index):
        """Set the tab index."""
        self.tab_index = tab_index

    def getTabIndex(self):
        """Return the tab index."""
        return self.tab_index


class GeneralTabPanel(TabWidget):
    """Class used to create the 'Geral' tab."""

    def __init__(
        self,
        RendaVariavel_df,
        RendaFixa_df,
        TesouroDireto_df,
        config_file,
    ):
        """Create the GeneralTabPanel object."""
        # Dataframes
        self.GeneralDataframes = GeneralDataframes(
            RendaVariavel_df,
            RendaFixa_df,
            TesouroDireto_df,
        )

        # Investment boxes
        self.config_file = config_file
        self.tree_list = []
        self.ClasseDeInvestimento = self.__createBoxTree(
            ClasseDeInvestimento,
            self.GeneralDataframes.getClasseDeInvestimentoDF(),
        )
        self.RendaVariavel = self.__createBoxTree(
            RendaVariavel,
            self.GeneralDataframes.getRendaVariavelDF(),
        )
        self.RendaFixa = self.__createBoxTree(
            RendaFixa,
            self.GeneralDataframes.getRendaFixaDF(),
        )
        self.TesouroDireto = self.__createBoxTree(
            TesouroDireto,
            self.GeneralDataframes.getTesouroDiretoDF(),
        )

        # 'Geral' tab widget
        super().__init__("Geral", self.tree_list)

    """Private methods."""

    def __createBoxTree(self, InvestmentConfigObj, dataframe=None):
        boxtree = BalancingBoxTreeview(
            self.config_file,
            InvestmentConfigObj,
            dataframe,
        )
        self.tree_list.append(boxtree.getTree())
        return boxtree

    """Public methods."""

    def resize(self):
        """Resize the treeviews."""
        for tree in self.tree_list:
            tree.resizeColumnsToTreeViewWidth()


class ConfigurationManager:
    """Class used to handle with configurations."""

    def __init__(self, extrato_path):
        """Create the ConfigurationManager object."""
        self.extrato_path = extrato_path
        self.config = InvestmentConfigManager(extrato_path)
        if self.config.isDefaultConfigFile():
            self.showDefatultConfigurationMsg()

    """Public methods."""

    def showDefatultConfigurationMsg(self):
        """Show the message related to default configuration file."""
        msg = "Um arquivo de configurações 'investimentos.ini' foi criado "
        msg += "no seguinte diretório:\n\n" + self.extrato_path
        msg += "\n\nConsidere editar esse arquivo conforme necessário."
        QMessageBox.information(
            self,
            "Análise de Portfólio",
            msg,
            QMessageBox.Ok,
        )

    def getConfigFile(self):
        """Return the configuration file."""
        return self.config.getConfigFile()


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
        self.ConfigurationManager = ConfigurationManager(extrato_path)

        # Tabs
        self.TabGroup = QtWidgets.QTabWidget()
        self.GeneralTabPanel = GeneralTabPanel(
            RendaVariavel_df,
            RendaFixa_df,
            TesouroDireto_df,
            self.ConfigurationManager.getConfigFile(),
        )
        self.TabGroup.addTab(
            self.GeneralTabPanel.getTab(),
            self.GeneralTabPanel.getTabTitle(),
        )

        # Set the window properties
        self.__setWindowProperties()

        # Show the window
        if auto_show:
            self.showMaximized()
            self.__resizeEvent()

    """Private methods."""

    def __setWindowProperties(self):
        spacing = Window.DEFAULT_BORDER_SIZE

        # Create the grid object
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid.setSpacing(spacing)
        self.grid.addWidget(self.TabGroup)

        # Set the grid layout
        self.setLayout(self.grid)

        # Set the title
        self.setWindowTitle("Balanceamento de Carteira")

    def __resizeEvent(self):
        self.GeneralTabPanel.resize()

    """Public methods."""

    def resizeEvent(self, event):
        """Overide the resizeEvent from QtWidgets.QWidget."""
        self.__resizeEvent()
