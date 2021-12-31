"""This file has a set of classes related to "QtWidgets.QTreeView"."""

from gui_lib.treeview.treeview import ResizableTreeview as ResTreeview
from gui_lib.treeview.treeview import Treeview
from gui_lib.treeview.treeview import TreeviewInterface as IntTreeview


class TreeviewPandas(Treeview):
    """Class used to create a special Treeview with "QtWidgets.QTreeView"."""

    def __init__(
        self,
        CentralWidget,
        PandasDataFrame,
        coordinate_X=IntTreeview.EMPTY_SPACE,
        coordinate_Y=IntTreeview.EMPTY_SPACE,
        width=IntTreeview.DEFAULT_WIDTH,
        height=IntTreeview.DEFAULT_HEIGHT,
    ):
        """Create a Treeview table object from "QtWidgets.QTreeView".

        Note: Fixed size and fixed coordinates.

        Arguments:
        - CentralWidget: the widget where the table will be placed
        - PandasDataFrame: the pandas dataframe
        - coordinate_X: the window X coordinate where the table will be placed
        - coordinate_Y: the window Y coordinate where the table will be placed
        - width: the width of the table
        - height: the height of the table
        """
        self.PandasDataFrame = PandasDataFrame
        super().__init__(
            CentralWidget=CentralWidget,
            columns_title_list=list(self.PandasDataFrame),
            coordinate_X=coordinate_X,
            coordinate_Y=coordinate_Y,
            width=width,
            height=height,
        )

    def showPandas(self, resize_per_contents=True):
        """Insert a Pandas Dataframe inside the Treeview."""
        for line_data_row in self.PandasDataFrame.itertuples(index=False):
            line_data_row_list = list(line_data_row)
            items_list = self.convertValuesListToItemsList(line_data_row_list)
            self.insertParentLine(items_list)
        if resize_per_contents:
            self.resizeColumnsToContents()

    def setDataframe(self, dataframe):
        """Set the dataframe."""
        self.PandasDataFrame = dataframe.copy()


class ResizableTreeviewPandas(ResTreeview):
    """Class used to create a special Treeview with "QtWidgets.QTreeView"."""

    def __init__(self, PandasDataFrame):
        """
        Create a Treeview table object from "QtWidgets.QTreeView".

        Arguments:
        - PandasDataFrame: the pandas dataframe
        """
        self.PandasDataFrame = PandasDataFrame
        super().__init__(
            columns_title_list=list(self.PandasDataFrame),
        )

    def showPandas(self, resize_per_contents=True):
        """Insert a Pandas Dataframe inside the Treeview."""
        for line_data_row in self.PandasDataFrame.itertuples(index=False):
            line_data_row_list = list(line_data_row)
            items_list = self.convertValuesListToItemsList(line_data_row_list)
            self.insertParentLine(items_list)
        if resize_per_contents:
            self.resizeColumnsToContents()

    def setDataframe(self, dataframe):
        """Set the dataframe."""
        self.PandasDataFrame = dataframe.copy()
