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
        main_title = self.investment.getMainTitle()
        value_list = self.__getValueList(type_list, dataframe, filter_column)
        self.box = BalancingBox(main_title)
        self.box.setValues(target_list, value_list, type_list)

        # Treeview
        format_df = self.box.getFormattedDataframe()
        filter_list = dataframe[filter_column].tolist()
        filter_list.extend(["TOTAL"])
        format_df = format_df[format_df[main_title].isin(filter_list)]
        self.tree = ResizableTreeviewPandas(format_df, split_big_title=False)
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
