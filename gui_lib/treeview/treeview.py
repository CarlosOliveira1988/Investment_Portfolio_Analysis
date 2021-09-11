"""This file has a set of classes related to "QtWidgets.QTreeView"."""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TreeviewInterface(QtWidgets.QTreeView):
    """Class used to create a Treeview table with "QtWidgets.QTreeView"."""

    # Contants related to the window
    EMPTY_SPACE = 20
    DEFAULT_WIDTH = 1100
    DEFAULT_HEIGHT = 660

    def __init__(
        self,
        CentralWidget=None,
        columns_title_list=[],
    ):
        """
        Create a Treeview table object from "QtWidgets.QTreeView".

        Arguments:
        - CentralWidget: the widget where the table will be placed
        - columns_title_list: a list of columns titles
        """
        if CentralWidget:
            super().__init__(CentralWidget)
        else:
            super().__init__()
        self.ColumnsTitleList = columns_title_list
        self.__createTreeViewModel(columns_title_list)
        self.setModel(self.TreeViewModel)

    def __splitBigTitle(self, title):
        return title.replace(" ", "\n")

    def __createTreeViewModel(self, columns_title_list):
        self.TreeViewModel = QStandardItemModel(
            0,
            len(columns_title_list),
            self,
        )
        for column_index in range(len(columns_title_list)):
            title = self.__splitBigTitle(columns_title_list[column_index])
            self.TreeViewModel.setHeaderData(
                column_index,
                Qt.Horizontal,
                title,
            )
            title_item = self.TreeViewModel.horizontalHeaderItem(column_index)
            title_item.setTextAlignment(Qt.AlignHCenter)

    def __createParentLine(self, parent_line_title):
        return QStandardItem(parent_line_title)

    def __insertParentLineData(self, parent_line_item, item_list):
        parent_line_item.appendRow(item_list)

    def insertParentLineItem(self, parent_line_title):
        """Insert a parent line item.

        Arguments:
        - parent_line_title: a string that represents the top-level of the
        tree-line

        Output:
        - parent_line_item: the ID (a "QStandardItem") of the first cell of
        a line
        """
        parent_line_item = self.__createParentLine(parent_line_title)
        self.insertParentLine(parent_line_item)
        return parent_line_item

    def insertChildrenLineData(self, parent_line_item, columns_value_list):
        """
        Insert a line of data in the second level of the "parent_line_item".

        Arguments:
        - parent_line_item: the ID of the first cell of a line
        - columns_value_list: a list of columns values (must have the same
        order and length of the columns titles)
        """
        item_list = self.convertValuesListToItemsList(columns_value_list)
        self.__insertParentLineData(parent_line_item, item_list)

    def convertValuesListToItemsList(self, columns_value_list):
        """
        Convert the values list to a items list.

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
        Insert a Parent Line Data.

        Usually, 'parent_line_item' may be used as 'items_list'.
        """
        self.TreeViewModel.appendRow(parent_line_item)

    def expandParentLines(self):
        """Expand all items."""
        self.expandAll()

    def collapseParentLines(self):
        """Collapse all items."""
        self.collapseAll()

    def resizeColumnsToContents(self):
        """Adjust the columns size according the columns contents."""
        for column_index in range(len(self.ColumnsTitleList)):
            self.resizeColumnToContents(column_index)

    def resizeColumnsToTreeViewWidth(self):
        """Adjust the columns size according the treeview width."""
        column_count = self.TreeViewModel.columnCount()
        column_width = round((self.width() - 25) / column_count)
        for column_index in range(column_count):
            self.setColumnWidth(column_index, column_width)


class Treeview(TreeviewInterface):
    """Class used to create a Treeview table with "QtWidgets.QTreeView"."""

    def __init__(
        self,
        CentralWidget,
        columns_title_list,
        coordinate_X=TreeviewInterface.EMPTY_SPACE,
        coordinate_Y=TreeviewInterface.EMPTY_SPACE,
        width=TreeviewInterface.DEFAULT_WIDTH,
        height=TreeviewInterface.DEFAULT_HEIGHT,
    ):
        """Create a Treeview table object from "QtWidgets.QTreeView".

        Note: Fixed size and fixed coordinates.

        Arguments:
        - CentralWidget: the widget where the table will be placed
        - columns_title_list: a list of columns titles
        - coordinate_X: the window X coordinate where the table will be placed
        - coordinate_Y: the window Y coordinate where the table will be placed
        - width: the width of the table
        - height: the height of the table
        """
        super().__init__(
            CentralWidget=CentralWidget,
            columns_title_list=columns_title_list,
        )
        self.setGeometry(
            QtCore.QRect(
                coordinate_X,
                coordinate_Y,
                width,
                height,
            )
        )


class ResizableTreeview(TreeviewInterface):
    """Class used to create a Treeview table with "QtWidgets.QTreeView"."""

    def __init__(self, columns_title_list):
        """
        Create a Treeview table object from "QtWidgets.QTreeView".

        Note: Dynamic size and dynamic coordinates for GridLayout.

        Arguments:
        - columns_title_list: a list of columns titles
        """
        super().__init__(
            CentralWidget=None,
            columns_title_list=columns_title_list,
        )
