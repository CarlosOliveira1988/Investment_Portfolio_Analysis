from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

from window import Window


class Treeview:
    """ 
    This class provides methods and attributes to create a treeview table.

    Arguments:
    - CentralWidget: the widget where the table will be placed
    - columns_title_list: a list of columns titles
    - coordinate_X: the window X coordinate where the table will be placed
    - coordinate_Y: the window Y coordinate where the table will be placed
    - width: the width of the table
    - height: the height of the table
    """

    # Contants related to the window
    DEFAULT_WIDTH = 1100
    DEFAULT_HEIGHT = 660

    def __init__(self, CentralWidget, columns_title_list, 
    coordinate_X=Window.DEFAULT_BORDER_SIZE, coordinate_Y=Window.DEFAULT_BORDER_SIZE, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        self.ColumnsTitleList = columns_title_list
        self.TreeView = QtWidgets.QTreeView(CentralWidget)
        self.TreeView.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        self.__createTreeViewModel(columns_title_list)
        self.TreeView.setModel(self.TreeViewModel)
        self.TreeViewWidth = width
        self.TreeViewHeigth = height

    """
    Private methods
    """
    def __splitBigTitle(self, title):
        return title.replace(' ', '\n')

    def __createTreeViewModel(self, columns_title_list):
        self.TreeViewModel = QStandardItemModel(0, len(columns_title_list), self.TreeView)
        for column_index in range(len(columns_title_list)):
            title = self.__splitBigTitle(columns_title_list[column_index])
            self.TreeViewModel.setHeaderData(column_index, Qt.Horizontal, title)
            title_item = self.TreeViewModel.horizontalHeaderItem(column_index)
            title_item.setTextAlignment(Qt.AlignHCenter)

    def __createParentLine(self, parent_line_title):
        return QStandardItem(parent_line_title)

    def __insertParentLineData(self, parent_line_item, item_list):
        parent_line_item.appendRow(item_list)

    """
    Public methods
    """
    def insertParentLineItem(self, parent_line_title):
        """
        Inserts a parent line item that represents the top-level of the tree-line

        Arguments:
        - parent_line_title: a string that represents the top-level of the line-tree

        Output:
        - parent_line_item: the ID (a "QStandardItem") of the first cell of a line
        """
        parent_line_item = self.__createParentLine(parent_line_title)
        self.insertParentLine(parent_line_item)
        return parent_line_item

    def insertChildrenLineData(self, parent_line_item, columns_value_list):
        """
        Inserts a line of data in the second level of the "parent_line_item".

        Arguments:
        - parent_line_item: the ID of the first cell of a line
        - columns_value_list: a list of columns values (must have the same order and length of the columns titles)
        """
        item_list = self.convertValuesListToItemsList(columns_value_list)
        self.__insertParentLineData(parent_line_item, item_list)

    def convertValuesListToItemsList(self, columns_value_list):
        """
        Converts the values list to a items list.

        Usually, 'items_list' may be used as 'parent_line_item'.
        """
        item_list = []
        for index in range(len(columns_value_list)):
            item = QStandardItem(str(columns_value_list[index]))
            item.setData(columns_value_list[index])
            item.setTextAlignment(Qt.AlignHCenter)
            item_list.append(item)
        return item_list

    def insertParentLine(self, parent_line_item):
        """
        Inserts a Parent Line Data.
        
        Usually, 'parent_line_item' may be used as 'items_list'.
        """
        self.TreeViewModel.appendRow(parent_line_item)
    
    def expandParentLines(self):
        """
        Expand all items.
        """
        self.TreeView.expandAll()

    def collapseParentLines(self):
        """
        Collapse all items.
        """
        self.TreeView.collapseAll()

    def resizeColumnsToContents(self):
        """
        Adjust the columns size according the columns contents.
        """
        for column_index in range(len(self.ColumnsTitleList)):
            self.TreeView.resizeColumnToContents(column_index)
    
    def resizeColumnsToTreeViewWidth(self):
        column_width = round(self.TreeViewWidth / self.TreeViewModel.columnCount())
        for column_index in range(self.TreeViewModel.columnCount()):
            self.TreeView.setColumnWidth(column_index, column_width)
