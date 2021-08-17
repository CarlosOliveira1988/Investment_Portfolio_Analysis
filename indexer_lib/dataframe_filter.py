class DataframeFilter:
    def __init__(self):
        pass

    def filterDataframePerColumn(self, dataframe, column_title, column_value):
        return dataframe[dataframe[column_title] == column_value]

    def filterDataframePerPeriod(
        self, dataframe, date_column_title, initial_date, final_date
    ):
        """
        Returns a filtered dataframe per 'initial' and 'final' dates.
        """
        return dataframe.loc[
            (dataframe[date_column_title] >= initial_date)
            & (dataframe[date_column_title] <= final_date)
        ]

    def getListFromDataframeColumn(self, dataframe, column_title):
        """
        Returns a list of data present in a column ('column_title') from a dataframe ('dataframe').

        Note: the 'column_title' must exist in the 'dataframe' and it is not included in the output list result.
        """
        return dataframe[column_title].tolist()
