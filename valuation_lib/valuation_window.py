"""This file has a class to show Valuation analysis frame."""

import sys

import pandas as pd
from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas
from gui_lib.window import Window
from PyQt5 import QtWidgets

from valuation_lib.fundamental_analysis import FundamentalAnalysisFrame
from valuation_lib.valuation_formater import FundamentalAnalysisFormater


class ValuationWindow(QtWidgets.QWidget):
    """Window Class used to show Valuation analysis frame."""

    def __init__(self, auto_show=True):
        """Create the ValuationWindow object.

        Arguments:
        - auto_show (True/False): flag to show window while creating the object
        """
        super().__init__()
        self.setWindowTitle("Indicadores Fundamentalistas")

        # Excel file under analysis
        self.file_path = sys.path[0]
        self.file_path += "\\valuation_lib\\analise_fundamentalista.xlsx"
        self.file_dataframe = pd.read_excel(self.file_path)

        # Analysis object
        self.analysis = FundamentalAnalysisFrame()
        self.analysis.setTickersList(list(self.file_dataframe["Ticker"]))
        self.analysis.updateTickersDataframe()

        # Formater
        self.formater = FundamentalAnalysisFormater(
            self.analysis.getTickersDataframe(),
        )
        self.formated_dataframe = self.formater.getFormattedDataFrame()

        # Treeview
        self.treeview = ResizableTreeviewPandas(self.formated_dataframe)
        self.treeview.showPandas()

        spacing = Window.DEFAULT_BORDER_SIZE
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid.setSpacing(spacing)
        self.grid.addWidget(self.treeview)
        self.setLayout(self.grid)

        # Show the window
        if auto_show:
            self.showMaximized()
            self.treeview.resizeColumnsToTreeViewWidth()

    def resizeEvent(self, event):
        """Overide the resizeEvent from QtWidgets.QWidget."""
        self.treeview.resizeColumnsToTreeViewWidth()
