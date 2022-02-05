"""This file has classes to show windows for portfolio balancing purpose."""

import sys

from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from PyQt5 import QtWidgets

from balance_lib.balance import BalancingBox
from balance_lib.get_config import (
    ClasseDeInvestimento,
    EnvironmentConfiguration,
    InvestmentConfigManager,
    RendaFixa,
    RendaVariavel,
    TesouroDireto,
)


class BalancingBoxTreeview:
    """Class used to create special treeview related to BalancingBox."""

    def __init__(self, config_file, InvestmentConfigObj):
        """Create the BalancingBoxTreeview object."""
        self.investment = InvestmentConfigObj(config_file)
        self.box = BalancingBox(self.investment.getMainTitle())
        self.tree = ResizableTreeviewPandas(
            self.box.getFormattedDataframe(),
            split_big_title=False,
        )
        self.tree.showPandas()

    def getTree(self):
        """Return the Tree object."""
        return self.tree


class BalancingWindow(QtWidgets.QWidget):
    """Window class used to show Balancing Portfolio frames."""

    def __init__(self, auto_show=True):
        """Create the BalancingWindow object.

        Arguments:
        - extrato_sheet_dir: the current extrato spreadsheet directory
        - auto_show (True/False): flag to show window while creating the object
        """
        super().__init__()

        # Configuration manager
        self.env_config = EnvironmentConfiguration()
        self.config = InvestmentConfigManager(self.env_config.getExtratoPath())
        self.config_file = self.config.getConfigFile()

        # ClasseDeInvestimento
        self.boxtree_list = []
        self.ClasseDeInvestimento = self.__createBoxTree(ClasseDeInvestimento)
        self.RendaVariavel = self.__createBoxTree(RendaVariavel)
        self.RendaFixa = self.__createBoxTree(RendaFixa)
        self.TesouroDireto = self.__createBoxTree(TesouroDireto)

        # Set the window properties
        self.__setWindowProperties()

        # Show the window
        if auto_show:
            self.showMaximized()
            self.__resizeEvent()

    def __resizeEvent(self):
        for boxtree in self.boxtree_list:
            boxtree.getTree().resizeColumnsToTreeViewWidth()

    def __createBoxTree(self, InvestmentConfigObj):
        boxtree = BalancingBoxTreeview(self.config_file, InvestmentConfigObj)
        self.boxtree_list.append(boxtree)
        return boxtree

    def __setWindowProperties(self):
        spacing = Window.DEFAULT_BORDER_SIZE

        # Create the grid object
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid.setSpacing(spacing)

        # Add the boxtree widgets
        for boxtree in self.boxtree_list:
            self.grid.addWidget(boxtree.getTree())

        # Set the grid layout
        self.setLayout(self.grid)

        # Set the title
        self.setWindowTitle("Balanceamento de Carteira")

    def resizeEvent(self, event):
        """Overide the resizeEvent from QtWidgets.QWidget."""
        self.__resizeEvent()
