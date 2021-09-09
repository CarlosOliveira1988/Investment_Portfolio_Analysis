"""This file has a set of classes related to "QtWidgets.QTreeView"."""

from gui_lib.treeview.treeview import Treeview


class TreeviewPandas(Treeview):
    """Class used to create a special Treeview with "QtWidgets.QTreeView"."""

    def __init__(
        self,
        CentralWidget=None,
        PandasDataFrame=None,
        coordinate_X=Treeview.EMPTY_SPACE,
        coordinate_Y=Treeview.EMPTY_SPACE,
        width=Treeview.DEFAULT_WIDTH,
        height=Treeview.DEFAULT_HEIGHT,
        autosize=False,
    ):
        """
        Create a Treeview table object from "QtWidgets.QTreeView".

        Arguments:
        - CentralWidget: the widget where the table will be placed
        - PandasDataFrame: the pandas dataframe
        """
        self.PandasDataFrame = PandasDataFrame
        if autosize:
            super().__init__(
                columns_title_list=list(self.PandasDataFrame),
                autosize=True,
            )
        else:
            super().__init__(
                CentralWidget,
                list(self.PandasDataFrame),
                coordinate_X,
                coordinate_Y,
                width,
                height,
                autosize=False,
            )

    def showPandas(self, resize_per_contents=True):
        """Insert a Pandas Dataframe inside the Treeview."""
        for line_data_row in self.PandasDataFrame.itertuples(index=False):
            line_data_row_list = list(line_data_row)
            items_list = self.convertValuesListToItemsList(line_data_row_list)
            self.insertParentLine(items_list)
        if resize_per_contents:
            self.resizeColumnsToContents()
