"""This file has a special class to format treeview tables."""

try:
    from gui_lib.treeview.treeview_format import (
        CurencyColumnType,
        DateColumnType,
        FloatColumnType,
        NonRequiredStringColumnType,
        PercentageColumnType,
        RequiredStringColumnType,
    )
except ModuleNotFoundError:
    from treeview_format import (
        CurencyColumnType,
        DateColumnType,
        FloatColumnType,
        NonRequiredStringColumnType,
        PercentageColumnType,
        RequiredStringColumnType,
    )

import pandas as pd


class TreeviewFormatApplier:
    """This class is useful to apply formats to Treeview.

    Basically, here we manipulate the dataframe to define:
    - the columns order
    - the column value types
    - the columns to be displayed
    """

    def __init__(self):
        """Create the formatter objct."""
        # Create the dataframe variables
        self.Dataframe = None
        self.FormatedDataFrame = None

        # Create the columns control lists
        self.column_type_list = []
        self.column_order = []
        self.currency_list = self.__newColumnList()
        self.date_list = self.__newColumnList()
        self.float_list = self.__newColumnList()
        self.percentage_list = self.__newColumnList()
        self.req_string_list = self.__newColumnList()
        self.nreq_string_list = self.__newColumnList()

    """
    Private methods
    """

    def __newColumnList(self):
        new_list = []
        self.column_type_list.append(new_list)
        return new_list

    def __fillNaValues(self):
        # Run per each list of types
        for column_type in self.column_type_list:

            # Run per each column of each type
            for column in column_type:
                column.fillNaDataFrameColumnValues(self.FormatedDataFrame)

    def __setColumnOrder(self):
        if self.column_order:
            self.FormatedDataFrame = self.FormatedDataFrame[self.column_order]

    def __format(self):
        # Run per each list of types
        for column_type in self.column_type_list:

            # Run per each column of each type
            for column in column_type:
                column.formatDataFrameColumnValues(self.FormatedDataFrame)

    def __getTypeList(self, title_list, column_type):
        type_list = []
        for title in title_list:
            type_list.append(column_type(title))
        return type_list

    """
    Public methods
    """

    def setDataframe(self, dataframe):
        """Set the dataframe."""
        self.Dataframe = dataframe
        self.FormatedDataFrame = dataframe

    def getColumnsTitleList(self):
        """Get the titles list."""
        return list(self.FormatedDataFrame)

    def getFormatedDataFrame(self):
        """Get the formated dataframe."""
        return self.FormatedDataFrame

    def runFormatter(self):
        """Apply the defined format to each column."""
        self.__setColumnOrder()
        self.__fillNaValues()
        self.__format()

    def setColumnOrder(self, title_list):
        """Define the columns order."""
        self.column_order = title_list

    def __setColumnTypeList(
        self,
        title_list,
        column_type,
        column_type_list,
    ):
        type_list = self.__getTypeList(
            title_list,
            column_type,
        )
        column_type_list.clear()
        column_type_list.extend(type_list)

    def setCurrencyType(self, title_list):
        """Define the columns to be displayed as currency.

        Empty cells will be displayed as '0.00'

        Argument:
        - title_list: a list of strings
        """
        self.__setColumnTypeList(
            title_list,
            CurencyColumnType,
            self.currency_list,
        )

    def setDateType(self, title_list):
        """Define the columns to be displayed as date.

        Empty cells will be displayed as ' '

        Argument:
        - title_list: a list of strings
        """
        self.__setColumnTypeList(
            title_list,
            DateColumnType,
            self.date_list,
        )

    def setFloatType(self, title_list):
        """Define the columns to be displayed as float values.

        Empty cells will be displayed as '0.00'

        Argument:
        - title_list: a list of strings
        """
        self.__setColumnTypeList(
            title_list,
            FloatColumnType,
            self.float_list,
        )

    def setPercentageType(self, title_list):
        """Define the columns to be displayed as percentage values.

        Empty cells will be displayed as ' '

        Argument:
        - title_list: a list of strings
        """
        self.__setColumnTypeList(
            title_list,
            PercentageColumnType,
            self.percentage_list,
        )

    def setRequiredString(self, title_list):
        """Define the columns to be displayed as required strings.

        Required strings means that empty cells will be displayed as 'NA'

        Argument:
        - title_list: a list of strings
        """
        self.__setColumnTypeList(
            title_list,
            RequiredStringColumnType,
            self.req_string_list,
        )

    def setNonRequiredString(self, title_list):
        """Define the columns to be displayed as non-required strings.

        Non-required strings means that empty cells will be displayed as ' '

        Argument:
        - title_list: a list of strings
        """
        self.__setColumnTypeList(
            title_list,
            NonRequiredStringColumnType,
            self.nreq_string_list,
        )


if __name__ == "__main__":

    # Dataframe for testing
    test_df = pd.DataFrame()
    test_df["Currency Column"] = [0.00, 1.00, 10.00]
    test_df["Date Column"] = ["01-01-2000", "01-01-2010", "01-01-2010"]
    test_df["Float Column"] = [0.00, 1.00, 10.00]
    test_df["Percentage Column"] = [0.10, 1.00, 10.00]
    test_df["Req-String Column"] = ["A", "B", "C"]
    test_df["NonReq-String Column"] = ["A", "B", "C"]
    print(test_df)

    # Formatter routine
    formatter = TreeviewFormatApplier()
    formatter.setDataframe(test_df)
    formatter.setCurrencyType(["Currency Column"])
    formatter.setFloatType(["Float Column"])
    formatter.setPercentageType(["Percentage Column"])
    formatter.runFormatter()
    print(formatter.getFormatedDataFrame())
