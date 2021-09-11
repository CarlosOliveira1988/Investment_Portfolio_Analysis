# """This file has a class to show Economic Indexers."""

# import sys

from gui_lib.window import Window
from PyQt5 import QtCore, QtWidgets

from indexer_lib.economic_indexers_widget import EconomicIndexerWidget


class EconomicIndexerWindow(Window):
    """Window Class used to how Economic Indexers."""

    def __init__(self, auto_show=True):
        """Create the EconomicIndexerWindow object.

        Arguments:
        - auto_show (True/False): flag to show window while creating the object
        """
        super().__init__("Indicadores Econômicos")

        # Indexer Widget
        self.IndexerWidget = EconomicIndexerWidget(self.getCentralWidget())

        # Window dimensions
        self.setGeometry(
            QtCore.QRect(
                0,
                0,
                self.IndexerWidget.getInternalWidth(),
                self.IndexerWidget.getInternalHeight(),
            )
        )
        self.setFixedSize(
            self.IndexerWidget.getInternalWidth(),
            self.IndexerWidget.getInternalHeight(),
        )

        # Show the window
        if auto_show:
            self.show()
