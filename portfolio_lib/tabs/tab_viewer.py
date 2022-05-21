"""File to handle the TAB visualization."""

import pandas as pd


class TabViewerInterface:
    """Tab Interface to work together with PortfolioViewerWidget."""

    def __init__(self):
        """Create the TabViewerInterface object."""
        pass

    def __sumValueColumn(self, dataframe, total_df, column_title):
        total_df[column_title] = [dataframe[column_title].sum()]

    def __sumPercentageColumn(self, total_df, percentage, initial, final):
        initial_value = total_df[initial].sum()
        final_value = total_df[final].sum()
        total_df[percentage] = [final_value / initial_value]

    def __makeUpColumns(self, total_df, target_column, columns_list, df):
        # Include the 'TOTAL' cell
        total_df[target_column] = ["TOTAL"]

        # All the column titles from the original dataframe
        all_df_columns_set = set(list(df))

        # All the columns with total values addded
        avoid_list = columns_list.copy()
        avoid_list.extend([target_column])

        # Fill with empty space ' ' the other columns
        target_empty_columns = all_df_columns_set.difference(avoid_list)
        for column in target_empty_columns:
            total_df[column] = ["-"]

    def addTotalLine(
        self,
        dataframe,
        columns_list,
        target_column,
        perc_lists=None,
    ):
        """Include a new line in the dataframe with the total values.

        Arguments:
        - dataframe: the dataframe with multiple columns
        - columns_list: the columns with 'simple sum' values
        - target_column: the column where the 'TOTAL' text will be inserted
        - perc_lists: a list of lists where:
          * 1st item: the percentage column title
          * 2nd item: the initial value column title
          * 3rd item: the final value column title
        """
        total_df = pd.DataFrame()

        # Sum the useful columns
        for column in columns_list:
            self.__sumValueColumn(dataframe, total_df, column)

        # Include the percentage columns
        if perc_lists:
            for perc in perc_lists:
                percentage_column = perc[0]
                initial_column = perc[1]
                final_column = perc[2]
                self.__sumPercentageColumn(
                    total_df,
                    percentage_column,
                    initial_column,
                    final_column,
                )

        # Make up the columns to avoid displaying unexpected N/A values
        avoid_list = []
        if perc_lists:
            for perc_list in perc_lists:
                avoid_list.extend(perc_list)
        avoid_list.extend(columns_list)
        avoid_list.extend([target_column])
        self.__makeUpColumns(total_df, target_column, avoid_list, dataframe)

        # Concatenate the dataframes
        dataframe = pd.concat(
            [dataframe, total_df],
            ignore_index=True,
            sort=False,
        )

        return dataframe

    def setNewData(self):
        """Abstract method to set new data."""
        pass

    def clearData(self):
        """Abstract method to clear data."""
        pass

    def updateData(self):
        """Abstract method to update data."""
        pass

    def onChangeAction(self):
        """Abstract method to execute onChange method."""
        pass

    def getTabIndex(self):
        """Abstract method to return the Tab index."""
        pass
