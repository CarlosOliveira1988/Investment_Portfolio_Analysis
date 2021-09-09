"""This file has a set of classes related to "QtWidgets.QMainWindow"."""

from PyQt5 import QtWidgets


class Window(QtWidgets.QMainWindow):
    """Class used to create a Window with "QtWidgets.QMainWindow"."""

    # Contants related to the window
    DEFAULT_WIDTH = 1200
    DEFAULT_HEIGHT = 675
    DEFAULT_BORDER_SIZE = 20

    def __init__(self, window_title):
        """
        Create a window object from "QtWidgets.QMainWindow".

        Arguments:
        - window_title: the title of the window
        """
        super().__init__()
        self.__setupWindow(window_title)

    def __setupWindow(self, window_title):
        self.CentralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.CentralWidget)
        self.setWindowTitle(window_title)

    def getCentralWidget(self):
        """
        Return the central widget of the window.

        All GUI components (buttons, checkboxes, tables, etc.) must have this
        widget as argument.
        """
        return self.CentralWidget
