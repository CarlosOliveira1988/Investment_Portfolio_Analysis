"""This is the main file of the project."""

import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from indexer_lib.economic_indexers_window import EconomicIndexerWindow
from portfolio_lib.portfolio_widget import PortfolioViewerWidget
from valuation_lib.valuation_window import ValuationWindow


class MainWindow(QtWidgets.QWidget):
    """Class used to create the Main Window of the project."""

    def __init__(self, file, auto_show=True):
        """Create the MainWindow object."""
        super().__init__()
        self.setWindowTitle("Análise de Portfólio")

        # Grid layout manager
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        # Add menu bar
        self._createActions()
        self._createMenuBar()

        # Portfolio widget
        self.PortfolioViewerWidget = PortfolioViewerWidget(file)
        self.grid.addWidget(self.PortfolioViewerWidget)

        # Status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.grid.addWidget(self.statusBar)
        self.statusBar.showMessage(file)

        # Show the window
        if auto_show:
            self.showMaximized()

    def __setAction(self, menu_tag, function):
        action = QtWidgets.QAction(menu_tag, self)
        action.triggered.connect(function)
        return action

    def _createActions(self):
        self.openAction = self.__setAction(
            "&Abrir Extrato",
            self._openFile,
        )

        self.exitAction = self.__setAction(
            "&Sair",
            self._exitApp,
        )

        self.exportGDAction = self.__setAction(
            "&Exportar Planilha Google Drive",
            self._exportGD,
        )

        self.aboutAction = self.__setAction(
            "&Sobre",
            self._aboutApp,
        )

        self.indexersAction = self.__setAction(
            "&Indicadores Econômicos",
            self._indexersApp,
        )

        self.valuationAction = self.__setAction(
            "&Indicadores Fundamentalistas",
            self._valuationApp,
        )

        self.focusReportAction = self.__setAction(
            "&Relatório Focus",
            self._focusReportLink,
        )

        self.fixedIncomeAction = self.__setAction(
            "&Simulador de Renda Fixa",
            self._fixedIncomeLink,
        )

        self.profitabilityAction = self.__setAction(
            "&Simulador de Rentabilidade",
            self._profitabilityLink,
        )

    def _createMenuBar(self):
        # Menu bar
        self.menuBar = QtWidgets.QMenuBar()
        self.grid.setMenuBar(self.menuBar)

        # File menu
        self.fileMenu = QtWidgets.QMenu("&Arquivo", self.menuBar)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.exportGDAction)
        self.fileMenu.addAction(self.exitAction)
        self.menuBar.addMenu(self.fileMenu)

        # Tools menu
        self.toolsMenu = QtWidgets.QMenu("&Ferramentas", self.menuBar)
        self.toolsMenu.addAction(self.indexersAction)
        self.toolsMenu.addAction(self.valuationAction)
        self.menuBar.addMenu(self.toolsMenu)

        # Links menu
        self.linksMenu = QtWidgets.QMenu("&Links", self.menuBar)
        self.linksMenu.addAction(self.focusReportAction)
        self.linksMenu.addAction(self.fixedIncomeAction)
        self.linksMenu.addAction(self.profitabilityAction)
        self.menuBar.addMenu(self.linksMenu)

        # Help menu
        self.helpMenu = QtWidgets.QMenu("&Ajuda", self.menuBar)
        self.helpMenu.addAction(self.aboutAction)
        self.menuBar.addMenu(self.helpMenu)

    def closeEvent(self, event):
        """Override 'QtWidgets.QWidget.closeEvent'."""
        event.accept()
        sys.exit()

    def _openFile(self):
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
            self.statusBar.showMessage(file_name)

    def _exportGD(self):
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

    def _exitApp(self):
        """Close the application."""
        sys.exit()

    def _indexersApp(self):
        self.EconomicIndexerWindow = EconomicIndexerWindow()

    def _valuationApp(self):
        self.ValuationWindow = ValuationWindow()

    def _focusReportLink(self):
        webbrowser.open(r"https://www.bcb.gov.br/publicacoes/focus")

    def _fixedIncomeLink(self):
        webbrowser.open(r"https://rendafixa.herokuapp.com")

    def _profitabilityLink(self):
        webbrowser.open(r"http://rendafixa.herokuapp.com/rentabilidade")

    def _aboutApp(self):
        pass


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
