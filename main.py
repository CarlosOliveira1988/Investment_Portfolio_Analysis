"""This is the main file of the project."""

import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from indexer_lib.economic_indexers_window import EconomicIndexerWindow
from portfolio_lib.portfolio_widget import PortfolioViewerWidget
from valuation_lib.valuation_window import ValuationWindow


class MenuInterface(QtWidgets.QMenu):
    """MenuInterface class for menus creation."""

    def __init__(self, tag_menu, menu_bar, function):
        """Create the MenuInterface object."""
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


class FileMenu(QtWidgets.QMenu):
    """FileMenu class."""

    def __init__(self, menu_bar, status_bar, PortfolioViewerWidget):
        """Create the FileMenu object."""
        super().__init__("&Arquivo", menu_bar)

        self.PortfolioViewerWidget = PortfolioViewerWidget
        self.status_bar = status_bar

        self.open = MenuInterface("&Abrir Extrato", menu_bar, self.openFile)
        self.addAction(self.open.getAction())

        self.exportGD = MenuInterface("&Exportar GD", menu_bar, self.exportGD)
        self.addAction(self.exportGD.getAction())

        self.exit = MenuInterface("&Sair", menu_bar, self.exitApp)
        self.addAction(self.exit.getAction())

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

    def exportGD(self):
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


class ToolsMenu(QtWidgets.QMenu):
    """ToolsMenu class."""

    def __init__(self, menu_bar):
        """Create the ToolsMenu object."""
        super().__init__("&Ferramentas", menu_bar)

        self.EconomicIndexerWindow = None
        self.ValuationWindow = None

        self.indexers = MenuInterface(
            "&Indicadores Econômicos",
            menu_bar,
            self.indexer,
        )
        self.addAction(self.indexers.getAction())

        self.valuation = MenuInterface(
            "&Indicadores Fundamentalistas",
            menu_bar,
            self.valuation,
        )
        self.addAction(self.valuation.getAction())

    def indexer(self):
        """Launch the EconomicIndexer app."""
        self.EconomicIndexerWindow = EconomicIndexerWindow()

    def valuation(self):
        """Launch the Valuation app."""
        self.ValuationWindow = ValuationWindow()


class LinksMenu(QtWidgets.QMenu):
    """LinksMenu class."""

    def __init__(self, menu_bar):
        """Create the LinksMenu object."""
        super().__init__("&Links", menu_bar)

        self.focus = MenuInterface(
            "&Relatório Focus",
            menu_bar,
            self.focusReportLink,
        )
        self.addAction(self.focus.getAction())

        self.fixedIncome = MenuInterface(
            "&Simulador de Renda Fixa",
            menu_bar,
            self.fixedIncomeLink,
        )
        self.addAction(self.fixedIncome.getAction())

        self.profitability = MenuInterface(
            "&Simulador de Rentabilidade",
            menu_bar,
            self.profitabilityLink,
        )
        self.addAction(self.profitability.getAction())

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

    def __init__(self, file, auto_show=True):
        """Create the MainWindow object."""
        super().__init__()
        self.setWindowTitle("Análise de Portfólio")

        # Grid layout manager
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        # Portfolio widget
        self.PortfolioViewerWidget = PortfolioViewerWidget(file)
        self.grid.addWidget(self.PortfolioViewerWidget)

        # Status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.grid.addWidget(self.statusBar)
        self.statusBar.showMessage(file)

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
        sys.exit()


if __name__ == "__main__":

    import sys

    SOURCE_FILE_DIRECTORY = sys.path[0] + "\\portfolio_lib"
    FILE_NAME = r"\PORTFOLIO_TEMPLATE.xlsx"
    FILE = SOURCE_FILE_DIRECTORY + FILE_NAME

    # Create the application
    import sys

    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)

    # File directory
    source_file_directory = sys.path[0]

    # Create and shows the "MainWindow" object
    main = MainWindow(FILE)

    # End the application when everything is closed
    sys.exit(app.exec_())
