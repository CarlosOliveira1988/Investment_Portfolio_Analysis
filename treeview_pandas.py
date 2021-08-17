from treeview import Treeview
from window import Window


class TreeviewPandas(Treeview):
    """
    This class provides methods and attributes to show Pandas DataFrames in a table.

    Arguments:
    - CentralWidget: the widget where the table will be placed
    - PandasDataFrame: the pandas dataframe
    """

    def __init__(
        self,
        CentralWidget,
        PandasDataFrame,
        coordinate_X=Window.DEFAULT_BORDER_SIZE,
        coordinate_Y=Window.DEFAULT_BORDER_SIZE,
        width=Treeview.DEFAULT_WIDTH,
        height=Treeview.DEFAULT_HEIGHT,
    ):
        self.PandasDataFrame = PandasDataFrame
        super().__init__(
            CentralWidget,
            list(self.PandasDataFrame),
            coordinate_X,
            coordinate_Y,
            width,
            height,
        )

    def showPandas(self, resize_per_contents=True):
        for line_data_row in self.PandasDataFrame.itertuples(index=False):
            line_data_row_list = list(line_data_row)
            items_list = self.convertValuesListToItemsList(line_data_row_list)
            self.insertParentLine(items_list)
            if resize_per_contents:
                self.resizeColumnsToContents()
