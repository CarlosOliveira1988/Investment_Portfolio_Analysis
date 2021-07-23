from PyQt5 import QtCore
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

from window import Window


class StandardTab:
    """ 
    This class is used to create a Standard Tab.

    Arguments:
    - CentralWidget: the widget where the tab will be placed
    - coordinate_X: the window X coordinate where the tab will be placed
    - coordinate_Y: the window Y coordinate where the tab will be placed
    - width: the width of the tab
    - height: the height of the tab
    """

    # Contants related to the tabs
    DEFAULT_WIDTH = 1100
    DEFAULT_HEIGHT = 660

    # Contants related to the internal tabs
    DEFAULT_INTERNAL_WIDTH = DEFAULT_WIDTH - 2*Window.DEFAULT_BORDER_SIZE
    DEFAULT_INTERNAL_HEIGHT = DEFAULT_HEIGHT - 3*Window.DEFAULT_BORDER_SIZE

    def __init__(self, CentralWidget, coordinate_X=0, coordinate_Y=0, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        self.__Tabs = QTabWidget(CentralWidget, )
        self.__Tabs.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        self.__Internal_Tab_Coordinate_X = coordinate_X + Window.DEFAULT_BORDER_SIZE
        self.__Internal_Tab_Coordinate_Y = coordinate_Y + Window.DEFAULT_BORDER_SIZE
        self.__Internal_Tab_Width = width - 2*Window.DEFAULT_BORDER_SIZE
        self.__Internal_Tab_Height = height - 2*Window.DEFAULT_BORDER_SIZE
    
    def addTab(self, tab_title):
        """
        Adds a new internal tab and returns its address.
        """
        new_tab = QWidget()
        new_tab.layout = QVBoxLayout()
        new_tab.setGeometry(QtCore.QRect(
            self.__Internal_Tab_Coordinate_X,
            self.__Internal_Tab_Coordinate_Y,
            self.__Internal_Tab_Width,
            self.__Internal_Tab_Height))
        self.__Tabs.addTab(new_tab, tab_title)
        return new_tab
