"""This file has a set of classes related to "QtWidgets.QTabWidget"."""

from PyQt5 import QtCore, QtWidgets


class StandardTab(QtWidgets.QTabWidget):
    """Class used to create a StandardTab with "QtWidgets.QTabWidget"."""

    # Contants related to the tabs
    DEFAULT_WIDTH = 1100
    DEFAULT_HEIGHT = 660

    # Contants related to the internal tabs
    EMPTY_SPACE = 20
    DEFAULT_INTERNAL_WIDTH = DEFAULT_WIDTH - 2 * EMPTY_SPACE
    DEFAULT_INTERNAL_HEIGHT = DEFAULT_HEIGHT - 3 * EMPTY_SPACE

    def __init__(
        self,
        CentralWidget,
        coordinate_X=0,
        coordinate_Y=0,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
    ):
        """
        Create an StandardTab object from "QtWidgets.QTabWidget".

        Arguments:
        - CentralWidget: the widget where the tab will be placed
        - coordinate_X: the window X coordinate inside the widget
        - coordinate_Y: the window Y coordinate inside the widget
        - width: the width of the tab
        - height: the height of the tab
        """
        super().__init__(CentralWidget)
        self.setGeometry(
            QtCore.QRect(
                coordinate_X,
                coordinate_Y,
                width,
                height,
            )
        )
        empty_space = StandardTab.EMPTY_SPACE
        self.__Internal_Tab_Coordinate_X = coordinate_X + empty_space
        self.__Internal_Tab_Coordinate_Y = coordinate_Y + empty_space
        self.__Internal_Tab_Width = width - 2 * empty_space
        self.__Internal_Tab_Height = height - 2 * empty_space

    def addNewTab(self, tab_title):
        """Add a new internal tab and return its object reference."""
        new_tab = QtWidgets.QWidget()
        new_tab.layout = QtWidgets.QVBoxLayout()
        new_tab.setGeometry(
            QtCore.QRect(
                self.__Internal_Tab_Coordinate_X,
                self.__Internal_Tab_Coordinate_Y,
                self.__Internal_Tab_Width,
                self.__Internal_Tab_Height,
            )
        )
        self.addTab(new_tab, tab_title)
        return new_tab
