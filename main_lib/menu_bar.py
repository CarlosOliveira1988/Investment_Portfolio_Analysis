"""This file is responsible to define the Menu Bar of the application."""

import sys

from PyQt5 import QtWidgets

from main_lib.file_menu import FileMenu
from main_lib.links_menu import LinksMenu
from main_lib.tools_menu import ToolsMenu


class MenuBar:
    """Class used to create the 'Menu Bar' of the main application."""

    def __init__(self, PortfolioViewerWidget, status_bar):
        """Create the MenuBar object."""
        self.PortfolioViewerWidget = PortfolioViewerWidget
        self.status_bar = status_bar
        self.extrato_file = self.PortfolioViewerWidget.getExtratoFile()

        # Menu bar
        self.menu = QtWidgets.QMenuBar()

        # File menu
        self.file_menu = FileMenu(
            self.menu,
            self.PortfolioViewerWidget,
            self.extrato_file,
            self.updateStatusBar,
            self.saveConfigAndclose,
        )
        self.menu.addMenu(self.file_menu)

        # Tools menu
        self.tools_menu = ToolsMenu(
            self.menu,
            self.PortfolioViewerWidget,
        )
        self.menu.addMenu(self.tools_menu)

        # Links menu
        self.links_menu = LinksMenu(
            self.menu,
        )
        self.menu.addMenu(self.links_menu)

    """Public methods."""

    def updateStatusBar(self, string):
        """Update the address string in the status bar."""
        self.status_bar.setBarMessage(string)

    def saveConfigAndclose(self):
        """Save the ENV file and close the application."""
        self.extrato_file = self.PortfolioViewerWidget.getExtratoFile()
        sys.exit()

    def getWidget(self):
        """Return the menu widget."""
        return self.menu

    def getExtratoFile(self):
        """Return the extrato file path."""
        return self.extrato_file

    def getFileMenu(self):
        """Return the File menu object."""
        return self.file_menu
