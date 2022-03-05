"""This file is useful to handle special treeviews for portfolio balancing."""

from gui_lib.treeview.treeview_pandas import ResizableTreeviewPandas

from balance_lib.balance import BalancingBox


class BalancingBoxTreeview:
    """Class used to create special treeview related to BalancingBox."""

    def __init__(
        self,
        InvestmentConfigObject,
        dataframe,
        immutable_type_list=False,
    ):
        """Create the BalancingBoxTreeview object.

        Arguments:
        - InvestmentConfigObject: any object related to the 'InvestmentConfig'
        class
        - dataframe: a short and filtered dataframe exported by the
        'PortfolioInvestment' class type, grouped per investment types, such
        as 'BDR', 'FII', 'Tesouro Direto', etc
        - immutable_type_list: due issues with special portuguese characters
        (present in 'Ações' word, for example), this flag is used to avoid
        unexpected conversions ('Ações' -> 'acoes')
        """
        # Main initialization
        self.investment = InvestmentConfigObject
        self.dataframe = dataframe.copy()
        self.immutable_type_list = immutable_type_list

        # Control initialization
        self.type_list = self.investment.getSubTitlesList()
        self.__setConfigurationVariables()

        # BalancingBox
        self.box = BalancingBox(self.main_title)
        self.box.setValues(self.target_list, self.value_list, self.type_list)

        # Treeview
        format_df = self.__getFormattedDataframe(
            self.dataframe.copy(),
            self.main_title,
            self.filter_column,
        )
        self.tree = ResizableTreeviewPandas(format_df, split_big_title=False)
        self.tree.showPandas()
        self.resize()

    """Private methods."""

    def __setConfigurationVariables(self):
        # this flag is used to avoid unexpected conversions
        # such as ('Ações' -> 'acoes') while handling the
        # configuration file reading/writing
        if not self.immutable_type_list:
            self.type_list = self.investment.getSubTitlesList()
        self.filter_column = self.investment.getFilterColumn()
        self.target_list = self.investment.getTargetList()
        self.main_title = self.investment.getMainTitle()
        self.value_list = self.__getValueList(
            self.type_list,
            self.dataframe.copy(),
            self.filter_column,
        )

    def __getFormattedDataframe(self, dataframe, main_title, filter_column):
        format_df = self.box.getFormattedDataframe()
        filter_list = dataframe[filter_column].tolist()
        filter_list.extend(["TOTAL"])
        return format_df[format_df[main_title].isin(filter_list)]

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

    def updateConfigurationValues(self):
        """Update configuration values from configuration file."""
        # Set the main control variables according to the configuration file
        self.__setConfigurationVariables()

        # Set the new parameters in the special dataframes
        self.box.setValues(self.target_list, self.value_list, self.type_list)

        # Set the treeview data
        format_df = self.__getFormattedDataframe(
            self.dataframe,
            self.main_title,
            self.filter_column,
        )
        self.tree.clearData()
        self.tree.setDataframe(format_df)
        self.tree.showPandas()
        self.resize()
