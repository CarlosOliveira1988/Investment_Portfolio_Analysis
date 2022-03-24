"""This is the main file of the project."""

import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from balance_lib.balance_window import BalancingWindow
from indexer_lib.economic_indexers_window import EconomicIndexerWindow
from main_config import ExtratoFileManager
from portfolio_lib.portfolio_widget import PortfolioViewerWidget
from valuation_lib.valuation_window import ValuationWindow


class SubMenu(QtWidgets.QMenu):
    """SubMenu class for menus creation."""

    def __init__(self, tag_menu, menu_bar, function):
        """Create the SubMenu object."""
        super().__init__(tag_menu, menu_bar)
        self.action = self.setAction(tag_menu, function)

    def setAction(self, menu_tag, function):
        """Set the related 'Action' to a specific 'menu'."""
        action = QtWidgets.QAction(menu_tag)
        action.triggered.connect(function)
        return action

    def getAction(self):
        """Return the 'Action'."""
        return self.action


class MenuInterface(QtWidgets.QMenu):
    """Interface to used while creating new menus for the application."""

    def __init__(self, menu_title, menu_bar):
        """Create the MenuInterface object."""
        super().__init__(menu_title, menu_bar)

    def addSubmenu(self, submenu_title, submenu_function):
        """Create the sub menu item."""
        sub_menu = SubMenu(
            submenu_title,
            self.menu_bar,
            submenu_function,
        )
        self.addAction(sub_menu.getAction())
        return sub_menu


class FileMenu(MenuInterface):
    """FileMenu class."""

    def __init__(self, menu_bar, status_bar, PortfolioViewerWidget):
        """Create the FileMenu object."""
        super().__init__("&Arquivo", menu_bar)
        self.menu_bar = menu_bar
        self.status_bar = status_bar
        self.PortfolioViewerWidget = PortfolioViewerWidget

        # Create the submenus
        self.open = self.addSubmenu(
            "&Abrir Extrato",
            self.openFile,
        )
        self.exportGD = self.addSubmenu(
            "&Exportar Planilha Google Drive",
            self.exportGDFile,
        )
        self.exit = self.addSubmenu(
            "&Sair",
            self.exitApp,
        )

    def openFile(self):
        """Open the 'Extrato' spreadsheet."""
        file_name_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Selecione o arquivo XLSX relacionado ao portfolio",
            sys.path[0],
            "xlsx(*.xlsx)",
        )
        file_name = file_name_tuple[0]
        if ".xlsx" in file_name:
            self.PortfolioViewerWidget.clearData()
            self.PortfolioViewerWidget.updateData(file_name)
            self.status_bar.showMessage(file_name)

    def exportGDFile(self):
        """Export the Google Drive spreadsheet."""
        try:
            self.PortfolioViewerWidget.exportGoogleDriveSheet()
            msg = "Planilha Google Drive exportada com sucesso.\n\n"
            QMessageBox.information(
                self,
                "Análise de Portfólio",
                msg,
                QMessageBox.Ok,
            )
        except AttributeError:
            msg = "Não foi possível exportar a planilha Google Drive."
            msg += "\n\nPlanilha extrato inválida."
            QMessageBox.warning(
                self,
                "Análise de Portfólio",
                msg,
                QMessageBox.Ok,
            )
        except PermissionError:
            msg = "Não foi possível exportar a planilha Google Drive."
            msg += "\n\nVerifique se o arquivo não está aberto."
            QMessageBox.warning(
                self,
                "Análise de Portfólio",
                msg,
                QMessageBox.Ok,
            )

    def exitApp(self):
        """Close the application."""
        sys.exit()


class ToolsMenu(MenuInterface):
    """ToolsMenu class."""

    def __init__(self, menu_bar, PortfolioViewerWidget):
        """Create the ToolsMenu object."""
        super().__init__("&Ferramentas", menu_bar)
        self.menu_bar = menu_bar
        self.PortfolioViewerWidget = PortfolioViewerWidget

        # Variables for External Windows
        self.EconomicIndexerWindow = None
        self.ValuationWindow = None
        self.BalancingWindow = None

        # Create the submenus
        self.indexers = self.addSubmenu(
            "&Indicadores Econômicos",
            self.indexerWin,
        )
        self.valuation = self.addSubmenu(
            "&Indicadores Fundamentalistas",
            self.valuationWin,
        )
        self.balancing = self.addSubmenu(
            "&Balanceamento de Carteira",
            self.balancingWin,
        )

    def indexerWin(self):
        """Launch the EconomicIndexer app."""
        self.EconomicIndexerWindow = EconomicIndexerWindow()

    def valuationWin(self):
        """Launch the Valuation app."""
        self.ValuationWindow = ValuationWindow()

    def balancingWin(self):
        """Launch the Portfolio Balancing app."""
        investment = self.PortfolioViewerWidget.getPortfolioInvestmentObject()
        extrato_path = self.PortfolioViewerWidget.getExtratoPath()
        self.BalancingWindow = BalancingWindow(
            investment.currentPortfolio(),
            investment.currentRendaFixa(),
            investment.currentTesouroDireto(),
            extrato_path,
        )


class LinksMenu(MenuInterface):
    """LinksMenu class."""

    def __init__(self, menu_bar):
        """Create the LinksMenu object."""
        super().__init__("&Links", menu_bar)
        self.menu_bar = menu_bar

        # Create the submenus
        self.focus = self.addSubmenu(
            "&Relatório Focus",
            self.focusReportLink,
        )
        self.fixedIncome = self.addSubmenu(
            "&Simulador de Renda Fixa",
            self.fixedIncomeLink,
        )
        self.profitability = self.addSubmenu(
            "&Simulador de Rentabilidade",
            self.profitabilityLink,
        )

    def focusReportLink(self):
        """Open the 'Relatorio Focus' weblink."""
        webbrowser.open(r"https://www.bcb.gov.br/publicacoes/focus")

    def fixedIncomeLink(self):
        """Open a weblink related to 'Renda Fixa'."""
        webbrowser.open(r"https://rendafixa.herokuapp.com")

    def profitabilityLink(self):
        """Open a weblink related to 'Rentabilidade'."""
        webbrowser.open(r"http://rendafixa.herokuapp.com/rentabilidade")


class MainWindow(QtWidgets.QWidget):
    """Class used to create the Main Window of the project."""

    def __init__(self, auto_show=True):
        """Create the MainWindow object."""
        super().__init__()
        self.setWindowTitle("Análise de Portfólio")

        # Define the Extrato spreadsheet file
        self.extrato_manager = ExtratoFileManager()
        self.extrato_file = self.extrato_manager.getExtratoFile()

        # Grid layout manager
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        # Portfolio widget
        self.PortfolioViewerWidget = PortfolioViewerWidget(self.extrato_file)
        self.grid.addWidget(self.PortfolioViewerWidget)

        # Status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.grid.addWidget(self.statusBar)
        self.statusBar.showMessage(self.extrato_file)

        # Add menu bar
        self._createMenuBar()

        # Show the window
        if auto_show:
            self.showMaximized()

    def _createMenuBar(self):
        # Menu bar
        self.menuBar = QtWidgets.QMenuBar()
        self.grid.setMenuBar(self.menuBar)

        # File menu
        self.fileMenu = FileMenu(
            self.menuBar,
            self.statusBar,
            self.PortfolioViewerWidget,
        )
        self.menuBar.addMenu(self.fileMenu)

        # Tools menu
        self.toolsMenu = ToolsMenu(
            self.menuBar,
            self.PortfolioViewerWidget,
        )
        self.menuBar.addMenu(self.toolsMenu)

        # Links menu
        self.linksMenu = LinksMenu(
            self.menuBar,
        )
        self.menuBar.addMenu(self.linksMenu)

    def closeEvent(self, event):
        """Override 'QtWidgets.QWidget.closeEvent'."""
        event.accept()
        extrato_file = self.PortfolioViewerWidget.getExtratoFile()
        self.extrato_manager.setExtratoFile(extrato_file)
        self.extrato_file = extrato_file
        sys.exit()


if __name__ == "__main__":

    import sys

    from PyQt5 import QtWidgets

    # Create the application
    app = QtWidgets.QApplication(sys.argv)

    # Create and show the "MainWindow" object
    main = MainWindow()

    # End the application when everything is closed
    sys.exit(app.exec_())
