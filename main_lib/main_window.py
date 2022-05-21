"""This file is responsible to define the main window of the application."""

import os

from portfolio_lib.portfolio_widget import PortfolioViewerWidget
from PyQt5 import QtWidgets

from main_lib.menu_bar import MenuBar
from main_lib.status_bar import StatusBar


class MainWindow(QtWidgets.QWidget):
    """Class used to create the Main Window of the project."""

    def __init__(self, extrato_file, auto_show=True):
        """Create the MainWindow object."""
        super().__init__()
        self.setWindowTitle("Análise de Portfólio")

        # Portfolio widget
        self.PortfolioWidget = PortfolioViewerWidget(extrato_file)

        # StatusBar widget
        self.status_bar = StatusBar()

        # MenuBar widget
        self.menu_bar = MenuBar(self.PortfolioWidget, self.status_bar)

        # Show the window
        self.__setupStatusBar()
        self.__setupGrid()
        if auto_show:
            self.showMaximized()

    """Private methods."""

    def __setupGrid(self):
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.PortfolioWidget)
        self.grid.addWidget(self.status_bar.getWidget())
        self.grid.setMenuBar(self.menu_bar.getWidget())
        self.setLayout(self.grid)

    def __setupStatusBar(self):
        # OnClick event
        file_menu = self.menu_bar.getFileMenu()
        self.status_bar.setUpdateButtonEvent(file_menu.reopenFile)
        self.status_bar.setEditXlsButtonEvent(self._openXlsFile)

        # Status bar message
        message = self.PortfolioWidget.getExtratoFile()
        self.status_bar.setBarMessage(message)

    """Overrides methods."""

    def closeEvent(self, event):
        """Override 'QtWidgets.QWidget.closeEvent'."""
        event.accept()

    """Protected methods."""

    def _openXlsFile(self):
        try:
            os.startfile(self.getExtratoFile())
        finally:
            pass

    """Puclic methods."""

    def getExtratoFile(self):
        """Get the extrato sheet file."""
        return self.PortfolioWidget.getExtratoFile()
