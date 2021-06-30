from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class DataViewerWindow(QtWidgets.QMainWindow):
    """
    This class provides methods and attributes to create a window.

    Arguments:
    - window_title: the title of the window
    """

    # Contants related to default window size
    DEFAULT_WIDTH = 1200
    DEFAULT_HEIGHT = 675

    def __init__(self, window_title):
        super().__init__()
        self.__setupWindow(window_title)
        self.__addWindowScrollBars()
        self.__setDefaultWindowSize()

    """
    Private methods
    """
    def __setupWindow(self, window_title):
        self.CentralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.CentralWidget)
        self.setWindowTitle(window_title)

    def __addWindowScrollBars(self):
        layout = QtWidgets.QVBoxLayout(self.CentralWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.ScrollArea = QtWidgets.QScrollArea(self.CentralWidget)
        self.ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        layout.addWidget(self.ScrollArea)
        self.ScrollAreaWidgetContents = QtWidgets.QWidget(self.CentralWidget)
        self.ScrollArea.setWidget(self.ScrollAreaWidgetContents)
        layout = QtWidgets.QHBoxLayout(self.ScrollAreaWidgetContents)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.CentralWidget)
        self.CentralWidget = self.ScrollAreaWidgetContents

    def __setDefaultWindowSize(self):
        self.CentralWidget.resize(DataViewerWindow.DEFAULT_WIDTH, DataViewerWindow.DEFAULT_HEIGHT)
        self.resize(DataViewerWindow.DEFAULT_WIDTH, DataViewerWindow.DEFAULT_HEIGHT)

    """
    Public methods
    """
    def getCentralWidget(self):
        """ 
        Returns the central widget of the window.

        All GUI components (buttons, checkboxes, tables, etc.) must have this widget as argument.
        """
        return self.CentralWidget
