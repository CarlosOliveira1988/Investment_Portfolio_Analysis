"""This file is useful to format the balancing dataframes."""


from gui_lib.treeview.format_applier import TreeviewFormatApplier


class BalancingBoxFormatter:
    """This class is useful to format BalancingBox dataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - dataframe: the pandas dataframe
    """

    def __init__(self, dataframe):
        """Create the BalancingBoxFormatter object."""
        first_column_title = list(dataframe)[0]
        self.formatter = TreeviewFormatApplier()
        self.formatter.setDataframe(dataframe)
        self.formatter.setRequiredString(
            [
                first_column_title,
            ]
        )
        self.formatter.setCurrencyType(
            [
                "Meta(R$)",
                "Atual(R$)",
                "Movimentação sugerida",
            ]
        )
        self.formatter.setPercentageType(
            [
                "Meta(%)",
                "Atual(%)",
            ]
        )
        self.formatter.setColumnOrder(
            [
                first_column_title,
                "Meta(%)",
                "Meta(R$)",
                "Atual(%)",
                "Atual(R$)",
                "Movimentação sugerida",
            ]
        )
        self.formatter.runFormatter()
        self.formattedDF = self.formatter.getFormatedDataFrame()

    """
    Public methods
    """

    def getColumnsTitleList(self):
        """Return a columns title list."""
        return list(self.formattedDF)

    def getFormattedDataFrame(self):
        """Return the formatted dataframe."""
        return self.formattedDF


class NewContributionBoxFormatter:
    """This class is useful to format NewContributionBox dataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - dataframe: the pandas dataframe
    """

    def __init__(self, dataframe):
        """Create the NewContributionBoxFormatter object."""
        first_column_title = list(dataframe)[0]
        self.formatter = TreeviewFormatApplier()
        self.formatter.setDataframe(dataframe)
        self.formatter.setRequiredString(
            [
                first_column_title,
            ]
        )
        self.formatter.setCurrencyType(
            [
                "Meta(R$)",
                "Atual(R$)",
                "Novo Aporte",
            ]
        )
        self.formatter.setPercentageType(
            [
                "Meta(%)",
                "Atual(%)",
            ]
        )
        self.formatter.setColumnOrder(
            [
                first_column_title,
                "Meta(%)",
                "Meta(R$)",
                "Atual(%)",
                "Atual(R$)",
                "Novo Aporte",
            ]
        )
        self.formatter.runFormatter()
        self.formattedDF = self.formatter.getFormatedDataFrame()

    """
    Public methods
    """

    def getColumnsTitleList(self):
        """Return a columns title list."""
        return list(self.formattedDF)

    def getFormattedDataFrame(self):
        """Return the formatted dataframe."""
        return self.formattedDF
