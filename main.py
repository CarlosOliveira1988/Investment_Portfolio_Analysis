"""This is the main file of the project."""

from PyQt5 import QtWidgets

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

    def _createActions(self):
        self.openAction = QtWidgets.QAction(
            "&Abrir Extrato",
            self,
        )
        self.openAction.triggered.connect(self._openFile)

        self.exitAction = QtWidgets.QAction(
            "&Sair",
            self,
        )
        self.exitAction.triggered.connect(self._exitApp)

        self.aboutAction = QtWidgets.QAction(
            "&Sobre",
            self,
        )
        self.aboutAction.triggered.connect(self._aboutApp)

        self.indexersAction = QtWidgets.QAction(
            "&Indicadores Econômicos",
            self,
        )
        self.indexersAction.triggered.connect(self._indexersApp)

        self.valuationAction = QtWidgets.QAction(
            "&Indicadores Fundamentalistas",
            self,
        )
        self.valuationAction.triggered.connect(self._valuationApp)

    def _createMenuBar(self):
        # Menu bar
        self.menuBar = QtWidgets.QMenuBar()
        self.grid.setMenuBar(self.menuBar)

        # File menu
        self.fileMenu = QtWidgets.QMenu("&Arquivo", self.menuBar)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.exitAction)
        self.menuBar.addMenu(self.fileMenu)

        # Tools menu
        self.toolsMenu = QtWidgets.QMenu("&Ferramentas", self.menuBar)
        self.toolsMenu.addAction(self.indexersAction)
        self.toolsMenu.addAction(self.valuationAction)
        self.menuBar.addMenu(self.toolsMenu)

        # Help menu
        self.helpMenu = QtWidgets.QMenu("&Ajuda", self.menuBar)
        self.helpMenu.addAction(self.aboutAction)
        self.menuBar.addMenu(self.helpMenu)

    def closeEvent(self, event):
        """Override 'QtWidgets.QWidget.closeEvent'."""
        event.accept()
        sys.exit()

    def _exitApp(self):
        """Close the application."""
        sys.exit()

    def _aboutApp(self):
        pass

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

    def _indexersApp(self):
        self.EconomicIndexerWindow = EconomicIndexerWindow()

    def _valuationApp(self):
        self.ValuationWindow = ValuationWindow()


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
