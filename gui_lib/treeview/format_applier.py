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
        self.formattedDF = None

        # Create the columns control lists
        self.column_type_list = []
        self.column_order = []
        self.currency_list = self.__newColumnList()
        self.date_list = self.__newColumnList()
        self.float_list = self.__newColumnList()
        self.percentage_list = self.__newColumnList()
        self.req_string_list = self.__newColumnList()
        self.nreq_string_list = self.__newColumnList()

    """Private methods."""

    def __newColumnList(self):
        new_list = []
        self.column_type_list.append(new_list)
        return new_list

    def __fillNaValues(self):
        # Run per each list of types
        for column_type in self.column_type_list:

            # Run per each column of each type
            for column in column_type:
                try:
                    column.fillNaDataFrameColumnValues(self.formattedDF)
                except KeyError:
                    pass

    def __setColumnOrder(self):
        if self.column_order:
            self.formattedDF = self.formattedDF[self.column_order]

    def __format(self):
        # Run per each list of types
        for column_type in self.column_type_list:

            # Run per each column of each type
            for column in column_type:
                try:
                    column.formatDataFrameColumnValues(self.formattedDF)
                except KeyError:
                    pass

    def __getTypeList(self, title_list, column_type):
        type_list = []
        for title in title_list:
            type_list.append(column_type(title))
        return type_list

    def __setColumnTypeList(self, title_list, column_type, column_type_list):
        type_list = self.__getTypeList(
            title_list,
            column_type,
        )
        column_type_list.clear()
        column_type_list.extend(type_list)

    """Public methods."""

    def setDataframe(self, dataframe):
        """Set the dataframe."""
        self.Dataframe = dataframe
        self.formattedDF = dataframe

    def getColumnsTitleList(self):
        """Get the titles list."""
        return list(self.formattedDF)

    def getFormatedDataFrame(self):
        """Get the formated dataframe."""
        return self.formattedDF

    def runFormatter(self):
        """Apply the defined format to each column."""
        self.__setColumnOrder()
        self.__fillNaValues()
        self.__format()

    def setColumnOrder(self, title_list):
        """Define the columns order."""
        self.column_order = title_list

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

    def setColumnStyles(self, column_type_dict):
        """Define the style and the order of all given columns.

        The 'column_type_dict' argument works as follows:
        {column_name1: column_type1}
        {column_name2: column_type2}
        ...
        {column_nameN: column_typeN}

        The following methods are called according to the dict value:
        - setCurrencyType():      '$'
        - setDateType():          '0-0'
        - setFloatType():         '0.0'
        - setPercentageType():    '%'
        - setRequiredString():    's'
        - setNonRequiredString(): 'ns'
        """
        # Declare the type lists
        setCurrencyType_list = []
        setDateType_list = []
        setFloatType_list = []
        setPercentageType_list = []
        setRequiredString_list = []
        setNonRequiredString_list = []
        columnOrder_list = []

        # Define the type lists
        for column, column_type in dict(column_type_dict).items():
            columnOrder_list.append(column)
            if column_type == "$":
                setCurrencyType_list.append(column)
            elif column_type == "0-0":
                setDateType_list.append(column)
            elif column_type == "0.0":
                setFloatType_list.append(column)
            elif column_type == "%":
                setPercentageType_list.append(column)
            elif column_type == "s":
                setRequiredString_list.append(column)
            elif column_type == "ns":
                setNonRequiredString_list.append(column)
            else:
                raise ValueError("Unknown column type.")

        # Set the column type
        self.setCurrencyType(setCurrencyType_list)
        self.setDateType(setDateType_list)
        self.setFloatType(setFloatType_list)
        self.setPercentageType(setPercentageType_list)
        self.setRequiredString(setRequiredString_list)
        self.setNonRequiredString(setNonRequiredString_list)

        # Set the column order
        self.setColumnOrder(columnOrder_list)


class EasyFormatter:
    """This class is useful to apply formats to Treeview.

    Basically, here we manipulate the dataframe to define:
    - the columns order
    - the column value types
    - the columns to be displayed
    """

    def __init__(self, dataframe, column_type_dict):
        """Create the EasyFormatter object."""
        self.dataframe = dataframe
        self.formatter = TreeviewFormatApplier()
        self.formatter.setDataframe(dataframe)
        self.formatter.setColumnStyles(column_type_dict)
        self.formatter.runFormatter()
        self.formattedDF = self.formatter.getFormatedDataFrame()

    def getColumnsTitleList(self):
        """Get the titles list."""
        return list(self.formattedDF)

    def getFormattedDataFrame(self):
        """Get the formated dataframe."""
        return self.formattedDF


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
    column_type_dict = {
        "Date Column": "0-0",
        "Currency Column": "$",
        "Percentage Column": "%",
        "Float Column": "0.0",
        "NonReq-String Column": "ns",
        "Req-String Column": "s",
    }
    formatter = TreeviewFormatApplier()
    formatter.setDataframe(test_df)
    formatter.setColumnStyles(column_type_dict)
    formatter.runFormatter()
    print(formatter.getFormatedDataFrame())
