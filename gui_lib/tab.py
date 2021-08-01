from PyQt5 import QtWidgets
from PyQt5 import QtCore

from window import Window


class StandardTab(QtWidgets.QTabWidget):
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
        super().__init__(CentralWidget)
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        self.__Internal_Tab_Coordinate_X = coordinate_X + Window.DEFAULT_BORDER_SIZE
        self.__Internal_Tab_Coordinate_Y = coordinate_Y + Window.DEFAULT_BORDER_SIZE
        self.__Internal_Tab_Width = width - 2*Window.DEFAULT_BORDER_SIZE
        self.__Internal_Tab_Height = height - 2*Window.DEFAULT_BORDER_SIZE
    
    def addNewTab(self, tab_title):
        """
        Adds a new internal tab and returns its address.
        """
        new_tab = QtWidgets.QWidget()
        new_tab.layout = QtWidgets.QVBoxLayout()
        new_tab.setGeometry(QtCore.QRect(
            self.__Internal_Tab_Coordinate_X,
            self.__Internal_Tab_Coordinate_Y,
            self.__Internal_Tab_Width,
            self.__Internal_Tab_Height))
        self.addTab(new_tab, tab_title)
        return new_tab
