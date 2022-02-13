"""This file is useful to handle special treeviews for portfolio balancing."""

from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas

from balance_lib.balance import BalancingBox


class BalancingBoxTreeview:
    """Class used to create special treeview related to BalancingBox."""

    def __init__(self, InvestmentConfigObject, dataframe):
        """Create the BalancingBoxTreeview object."""
        self.investment = InvestmentConfigObject

        # BalancingBox
        filter_column = self.investment.getFilterColumn()
        target_list = self.investment.getTargetList()
        type_list = self.investment.getSubTitlesList()
        value_list = self.__getValueList(type_list, dataframe, filter_column)
        self.box = BalancingBox(self.investment.getMainTitle())
        self.box.setValues(target_list, value_list, type_list)

        # Treeview
        self.tree = ResizableTreeviewPandas(
            self.box.getFormattedDataframe(),
            split_big_title=False,
        )
        self.tree.showPandas()
        self.resize()

    """Private methods."""

    def __getValueList(self, type_list, dataframe, filter_column):
        value_list = []
        for invest_type in type_list:
            df = dataframe[dataframe[filter_column] == invest_type]
            value = df["Preço mercado"].sum()
            value_list.append(value)
        return value_list

    """Public methods."""

    def getTree(self):
        """Return the Tree object."""
        return self.tree

    def resize(self):
        """Resize the treeview."""
        self.tree.resizeColumnsToTreeViewWidth()
