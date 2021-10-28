"""This file has some common filters related to pandas dataframes."""

from datetime import datetime

import pandas as pd


class DataframeFilter:
    """Class used to filter pandas dataframes."""

    def __init__(self):
        """Create the DataframeFilter object."""
        pass

    def _checkDataframeType(self, dataframe):
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "The dataframe argument should be a pandas dataframe.",
            )

    def _checkColumnNameType(self, column_title):
        if not isinstance(column_title, str):
            raise TypeError(
                "The column_title argument should be a string.",
            )

    def _checkDateType(self, date):
        if not isinstance(date, datetime):
            raise TypeError(
                "The date_column argument should be a datetime type.",
            )

    def filterDataframePerColumn(self, dataframe, column_title, column_value):
        """Return a filtered dataframe given a column title and value.

        If the column title does not exist, then return the dataframe.
        """
        self._checkDataframeType(dataframe)
        self._checkColumnNameType(column_title)
        try:
            return dataframe[dataframe[column_title] == column_value]
        except KeyError:
            return dataframe

    def filterDataframePerPeriod(
        self, dataframe, date_column_title, initial_date, final_date
    ):
        """Return a filtered dataframe per 'initial' and 'final' dates.

        If the column title does not exist, then return the dataframe.
        """
        self._checkDataframeType(dataframe)
        self._checkColumnNameType(date_column_title)
        self._checkDateType(initial_date)
        self._checkDateType(final_date)
        try:
            return dataframe.loc[
                (dataframe[date_column_title] >= initial_date)
                & (dataframe[date_column_title] <= final_date)
            ]
        except KeyError:
            return dataframe

    def getListFromDataframeColumn(self, dataframe, column_title):
        """Return a list of data present in a given column.

        If the column title does not exist, then return an empty list.
        """
        self._checkDataframeType(dataframe)
        self._checkColumnNameType(column_title)
        try:
            return dataframe[column_title].tolist()
        except KeyError:
            return []
