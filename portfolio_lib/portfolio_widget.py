"""This file has a set of classes to display data from Portfolio."""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from xlrd import XLRDError

from portfolio_lib.portfolio_investment import PortfolioInvestment
from portfolio_lib.tabs.extrato_tab import ExtratoTabInterface
from portfolio_lib.tabs.fixed_income_tab import FixedIncomeTabInterface
from portfolio_lib.tabs.short_summary_tab import ShortSummaryTabInterface
from portfolio_lib.tabs.treasuries_tab import TreasuriesTabInterface
from portfolio_lib.tabs.variable_income_tab import VariableTabInterface


class PortfolioViewerWidget(QtWidgets.QTabWidget):
    """Widget used to show data related to Portfolio."""

    def __init__(self, File):
        """Create the PortfolioViewerWidget object.

        Arguments:
        - File: the Portfolio file
        """
        super().__init__()
        self.investment = PortfolioInvestment(File)
        self.__createTabs()
        self.setPortfolioInvestment(File, initialization=True)
        self.__addDataToTabs()

        # Connect tab event
        self.currentChanged.connect(self.onChange)

    def __setMainDataframes(self):
        self.extrato = self.investment.getExtrato()
        self.variable_income = self.investment.currentPortfolio()
        self.fixed_income = self.investment.currentRendaFixa()
        self.treasuries = self.investment.currentTesouroDireto()
        self.short_summary = self.extrato.copy()

    def __updateMainDataframes(self, initialization):
        try:
            if not initialization:
                self.investment.run()
            self.__setMainDataframes()
            if self.investment.isValidFile():
                return True
            else:
                self.__showColumnsErrorMessage()
                return False
        except XLRDError:
            self.__setMainDataframes()
            self.__showXLRDErrorMessage()
            return False

    def __addNewTab(self, tab_widget):
        tab_index = self.addTab(
            tab_widget.getTab(),
            tab_widget.getTabTitle(),
        )
        tab_widget.setTabIndex(tab_index)
        return tab_index

    def __showColumnsErrorMessage(self):
        msg = "O arquivo selecionado é inválido.\n\n"
        msg += "Por favor, verifique se as colunas existem no arquivo:\n"
        for title in self.investment.getExpectedColumnsTitleList():
            msg += "\n - " + title
        QMessageBox.warning(self, "Análise de Portfólio", msg, QMessageBox.Ok)

    def __showXLRDErrorMessage(self):
        msg = "O arquivo selecionado é inválido.\n\n"
        msg += "Por favor, verifique se o arquivo contém apenas 1 aba."
        QMessageBox.warning(self, "Análise de Portfólio", msg, QMessageBox.Ok)

    def __setTabInterfaceList(self):
        self.TabInterfaceList = [
            self.ExtratoTab,
            self.VariableTab,
            self.FixedTab,
            self.TreasuriesTab,
            self.ShortSummaryTab,
        ]

    def __setTabDataframeList(self):
        self.TabDataframeList = [
            self.extrato,
            self.variable_income,
            self.fixed_income,
            self.treasuries,
            self.short_summary,
        ]

    def setPortfolioInvestment(self, File, initialization=False):
        """Read the excel file and update the main dataframes."""
        self.File = File
        if not initialization:
            self.investment.setFile(self.File)
        df_updated_flag = self.__updateMainDataframes(initialization)
        self.__setTabDataframeList()
        return df_updated_flag

    def exportGoogleDriveSheet(self):
        """Export the Google Drive spreasheet."""
        self.investment.currentPortfolioGoogleDrive()

    def __createTabs(self):
        self.ExtratoTab = ExtratoTabInterface(self.__addNewTab)
        self.VariableTab = VariableTabInterface(self.__addNewTab)
        self.FixedTab = FixedIncomeTabInterface(self.__addNewTab)
        self.TreasuriesTab = TreasuriesTabInterface(self.__addNewTab)
        self.ShortSummaryTab = ShortSummaryTabInterface(self.__addNewTab)
        self.__setTabInterfaceList()

    def __addDataToTabs(self):
        self.ExtratoTab.setNewData(self.extrato)
        self.VariableTab.setNewData(self.variable_income)
        self.FixedTab.setNewData(self.fixed_income)
        self.TreasuriesTab.setNewData(self.treasuries)
        self.ShortSummaryTab.setNewData(self.short_summary)

    def clearData(self):
        """Clear the treeview data lines."""
        for tab_interface in self.TabInterfaceList:
            tab_interface.clearData()

    def updateData(self, File):
        """Update the treeview data lines."""
        if self.setPortfolioInvestment(File):
            for index in range(len(self.TabInterfaceList)):
                tab_interface = self.TabInterfaceList[index]
                tab_dataframe = self.TabDataframeList[index]
                tab_interface.updateData(tab_dataframe)
            self.File = File

    def onChange(self, index):
        """Onchange tab method to render the table columns."""
        for tab_interface in self.TabInterfaceList:
            if index == tab_interface.getTabIndex():
                tab_interface.onChangeAction()

    def getPortfolioInvestmentObject(self):
        """Return the Portfolio Investment Object to handle extrato sheet."""
        return self.investment

    def getExtratoPath(self):
        """Get the extrato sheet path."""
        return self.investment.getExtratoPath()

    def getExtratoFile(self):
        """Get the extrato sheet file."""
        return self.File
