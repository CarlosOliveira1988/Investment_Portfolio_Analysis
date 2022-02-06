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
        value_list = self.__getValueList(
            type_list,
            dataframe,
            filter_column,
        )
        self.box = BalancingBox(self.investment.getMainTitle())
        self.box.setValues(target_list, value_list, type_list)

        # Treeview
        self.tree = ResizableTreeviewPandas(
            self.box.getFormattedDataframe(),
            split_big_title=False,
        )
        self.tree.showPandas()

    def __getValueList(self, type_list, dataframe, filter_column):
        value_list = []
        for invest_type in type_list:
            df = dataframe[dataframe[filter_column] == invest_type]
            value = df["Preço mercado"].sum()
            value_list.append(value)
        return value_list

    def getTree(self):
        """Return the Tree object."""
        return self.tree


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

        # Main dataframes
        self.RendaVariavel_df = RendaVariavel_df
        self.RendaFixa_df = RendaFixa_df
        self.TesouroDireto_df = TesouroDireto_df
        self.ClasseDeInvestimento_df = self.__getClasseDeInvestimentoDF()

        # Configuration manager
        self.config = InvestmentConfigManager(extrato_path)
        self.config_file = self.config.getConfigFile()
        if self.config.isDefaultConfigFile():
            msg = "Um arquivo de configurações 'investimentos.ini' foi criado "
            msg += "no seguinte diretório:\n\n" + extrato_path
            msg += "\n\nConsidere editar esse arquivo conforme necessário."
            QMessageBox.information(
                self,
                "Análise de Portfólio",
                msg,
                QMessageBox.Ok,
            )

        # Investment boxtree's
        self.boxtree_list = []
        self.ClasseDeInvestimento = self.__createBoxTree(
            ClasseDeInvestimento,
            self.ClasseDeInvestimento_df,
        )
        self.RendaVariavel = self.__createBoxTree(
            RendaVariavel,
            self.RendaVariavel_df,
        )
        self.RendaFixa = self.__createBoxTree(
            RendaFixa,
            self.RendaFixa_df,
        )
        self.TesouroDireto = self.__createBoxTree(
            TesouroDireto,
            self.TesouroDireto_df,
        )

        # Set the window properties
        self.__setWindowProperties()

        # Show the window
        if auto_show:
            self.showMaximized()
            self.__resizeEvent()

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

    def __resizeEvent(self):
        for boxtree in self.boxtree_list:
            boxtree.getTree().resizeColumnsToTreeViewWidth()

    def __createBoxTree(self, InvestmentConfigObj, dataframe=None):
        boxtree = BalancingBoxTreeview(
            self.config_file,
            InvestmentConfigObj,
            dataframe,
        )
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
