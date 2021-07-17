from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5 import QtCore

from economic_indexers import EconomicIndexer
from treeview_pandas import TreeviewPandas
from window import Window


class StandardTab:

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
    
    def addTab(self, tab_title):
        new_tab = QWidget()
        new_tab.layout = QVBoxLayout()
        new_tab.setGeometry(QtCore.QRect(
            self.__Internal_Tab_Coordinate_X, 
            self.__Internal_Tab_Coordinate_Y,
            StandardTab.DEFAULT_INTERNAL_WIDTH, 
            StandardTab.DEFAULT_INTERNAL_HEIGHT))
        self.__Tabs.addTab(new_tab, tab_title)
        return new_tab


class EconomicIndexerWidget:

    def __init__(self, CentralWidget):
        self.Indexers = EconomicIndexer()
        self.__Tab = StandardTab(CentralWidget)
        self.__addTabs()

    def __addTabs(self):
        for name in self.Indexers.getNamesList():
            tab_central_widget = self.__Tab.addTab(name)
            dataframe = self.Indexers.__getattribute__(name).getFormatedDataframe(False)
            new_treeview = TreeviewPandas(tab_central_widget, dataframe, width=StandardTab.DEFAULT_INTERNAL_WIDTH, height=StandardTab.DEFAULT_INTERNAL_HEIGHT)
            new_treeview.showPandas()
            new_treeview.resizeColumnsToTreeViewWidth()
