from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem


class DataViewerTable:
    """ 
    This class provides methods and attributes to create a treeview table.

    Arguments:
    - DataViewerWindow: the DataViewerWindow window object
    - columns_title_list: a list of columns titles
    """
    def __init__(self, DataViewerWindow, columns_title_list):
        self.TreeView = QtWidgets.QTreeView(DataViewerWindow.getCentralWidget())
        self.TreeView.setGeometry(
            QtCore.QRect(0, 0, DataViewerWindow.DEFAULT_WIDTH, DataViewerWindow.DEFAULT_HEIGHT)
        )
        self.TreeViewModel = QStandardItemModel(0, len(columns_title_list), self.TreeView)
        for column_index in range(len(columns_title_list)):
            self.TreeViewModel.setHeaderData(column_index, Qt.Horizontal, columns_title_list[column_index])
        self.TreeView.setModel(self.TreeViewModel)

    """
    Private methods
    """
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
            item_list.append(item)
        return item_list

    def insertParentLine(self, parent_line_item):
        """
        Inserts a Parent Line Data.
        
        Usually, 'parent_line_item' may be used as 'items_list'.
        """
        self.TreeViewModel.appendRow(parent_line_item)
