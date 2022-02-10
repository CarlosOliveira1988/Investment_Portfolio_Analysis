"""This file has a special widget based on "QtWidgets.QWidget"."""

from PyQt5 import QtWidgets


class TabViewerWidget:
    """Widget used to show tabs related to PortfolioViewerWidget."""

    def __init__(self, special_widget_list, tab_title, spacing=0):
        """Create the TabViewerWidget object.

        The 'special_widget_list' argument is a list of any widgets
        based on the 'QtWidgets.QWidget' class.

        The 'tab_title' is the text on the tab.
        """
        self.tab_title = tab_title
        self.tab = QtWidgets.QWidget()
        self.grid_tab = QtWidgets.QGridLayout()
        self.grid_tab.setContentsMargins(
            spacing,
            spacing,
            spacing,
            spacing,
        )
        self.grid_tab.setSpacing(spacing)
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
