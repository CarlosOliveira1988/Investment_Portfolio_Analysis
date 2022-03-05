"""This file is useful to format the balancing dataframes."""


from gui_lib.treeview.format_applier import EasyFormatter


class BalancingBoxFormatter(EasyFormatter):
    """This class is useful to format BalancingBox dataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - dataframe: the pandas dataframe
    """

    def __init__(self, dataframe):
        """Create the BalancingBoxFormatter object."""
        first_column_title = list(dataframe)[0]
        column_type_dict = {
            first_column_title: "s",
            "Meta(%)": "%",
            "Meta(R$)": "$",
            "Atual(%)": "%",
            "Atual(R$)": "$",
            "Movimentação sugerida": "$",
        }
        super().__init__(dataframe, column_type_dict)


class NewContributionBoxFormatter(EasyFormatter):
    """This class is useful to format NewContributionBox dataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - dataframe: the pandas dataframe
    """

    def __init__(self, dataframe):
        """Create the NewContributionBoxFormatter object."""
        first_column_title = list(dataframe)[0]
        column_type_dict = {
            first_column_title: "s",
            "Meta(%)": "%",
            "Meta(R$)": "$",
            "Atual(%)": "%",
            "Atual(R$)": "$",
            "Novo Aporte": "$",
        }
        super().__init__(dataframe, column_type_dict)
