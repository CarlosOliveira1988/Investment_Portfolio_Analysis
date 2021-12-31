"""This file has a set of classes to format the treeviews."""

import locale
from datetime import datetime

import pandas as pd


class TreeviewValueFormat:
    """A collection of methods to format single values.

    It formats as follows:
    - Date: 2021/06/27
    - Float: 1.00
    - Percentage: 1.00%
    - Currency: R$ 1,00
    - String: String
    """

    def setDateFormat(datestr):
        """Set the value as Date."""
        if isinstance(datestr, pd.Timestamp) or isinstance(datestr, datetime):
            return str(datestr.strftime("%Y/%m/%d"))
        else:
            return datestr

    def setDateTimeFormat(datestr):
        """Set the value as DateTime."""
        if isinstance(datestr, pd.Timestamp) or isinstance(datestr, datetime):
            return str(datestr.strftime("%Y/%m/%d %H:%M:%S"))
        else:
            return datestr

    def setFloatFormat(float_value):
        """Set the value as Float with 2 decimals."""
        if isinstance(float_value, float) or isinstance(float_value, int):
            return "{0:.2f}".format(float(float_value))
        else:
            return float_value

    def setPercentageFormat(perc_value):
        """Set the value as percentage with 2 decimals."""
        if isinstance(perc_value, float) or isinstance(perc_value, int):
            return "{0:.2f}%".format(float(perc_value) * 100)
        else:
            return perc_value

    def setCurrencyFormat(currency_val):
        """Set the value as Currency."""
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        if isinstance(currency_val, float) or isinstance(currency_val, int):
            return locale.currency(float(currency_val), grouping=True)
        else:
            return currency_val

    def setStringFormat(string_value):
        """Set the value as string."""
        return str(string_value)


class TreeviewDataframeFormat:
    """A collection of methods to format dataframe column values.

    It formats as follows:
    - Date: 2021-06-27
    - Float: 1.00
    - Percentage: 1.00%
    - Currency: R$ 1,00
    - String: String
    """

    def setDateFormat(data_frame, date_column):
        """Set the column as Date."""
        date_list = [
            TreeviewValueFormat.setDateFormat(datestr)
            for datestr in list(data_frame[date_column])
        ]
        data_frame[date_column] = date_list

    def setFloatFormat(data_frame, float_column):
        """Set the column as Float."""
        float_list = [
            TreeviewValueFormat.setFloatFormat(float_value)
            for float_value in list(data_frame[float_column])
        ]
        data_frame[float_column] = float_list

    def setPercentageFormat(data_frame, percentage_column):
        """Set the column as Percentage."""
        percentage_list = [
            TreeviewValueFormat.setPercentageFormat(perc_value)
            for perc_value in list(data_frame[percentage_column])
        ]
        data_frame[percentage_column] = percentage_list

    def setCurrencyFormat(data_frame, currency_column):
        """Set the column as Currency."""
        currency_list = [
            TreeviewValueFormat.setCurrencyFormat(currency_val)
            for currency_val in list(data_frame[currency_column])
        ]
        data_frame[currency_column] = currency_list

    def setStringFormat(data_frame, string_column):
        """Set the column as String."""
        string_list = [
            TreeviewValueFormat.setStringFormat(string_value)
            for string_value in list(data_frame[string_column])
        ]
        data_frame[string_column] = string_list


class TreeviewColumn:
    """A collection of methods and attributes to format dataframe columns.

    It formats as follows:
    - Date: 2021-06-27
    - Float: 1.00
    - Percentage: 1.00%
    - Currency: R$ 1,00
    - String: String

    Arguments:
    - title: the column title
    - format_type: the column format (date/float/percentage/currency/string)
    - na_value: the string used to fill na values (example: 'R$ 0.00')
    """

    def __init__(self, title, format_type, na_value):
        """Create the TreeviewColumn object."""
        self.Title = title
        self.FormatType = format_type
        self.NaValue = na_value

    def formatValue(self, value):
        """Format the value as specified in the object initialization."""
        if self.FormatType == "date":
            return TreeviewValueFormat.setDateFormat(value)
        elif self.FormatType == "float":
            return TreeviewValueFormat.setFloatFormat(value)
        elif self.FormatType == "percentage":
            return TreeviewValueFormat.setPercentageFormat(value)
        elif self.FormatType == "currency":
            return TreeviewValueFormat.setCurrencyFormat(value)
        elif self.FormatType == "string":
            return TreeviewValueFormat.setStringFormat(value)

    def formatDataFrameColumnValues(self, data_frame):
        """Format the column as specified in the object initialization."""
        if self.FormatType == "date":
            TreeviewDataframeFormat.setDateFormat(data_frame, self.Title)
        elif self.FormatType == "float":
            TreeviewDataframeFormat.setFloatFormat(data_frame, self.Title)
        elif self.FormatType == "percentage":
            TreeviewDataframeFormat.setPercentageFormat(data_frame, self.Title)
        elif self.FormatType == "currency":
            TreeviewDataframeFormat.setCurrencyFormat(data_frame, self.Title)
        elif self.FormatType == "string":
            TreeviewDataframeFormat.setStringFormat(data_frame, self.Title)

    def fillNaDataFrameColumnValues(self, data_frame):
        """Fill the NA values as specified in the object initialization."""
        data_frame[self.Title].fillna(value=self.NaValue, inplace=True)

    def getTitle(self):
        """Return the column title."""
        return self.Title


class RequiredStringColumnType(TreeviewColumn):
    """Class to format columns with the String format."""

    def __init__(self, title):
        """Create the RequiredStringColumnType object."""
        super(RequiredStringColumnType, self).__init__(title, "string", "NA")


class NonRequiredStringColumnType(TreeviewColumn):
    """Class to format columns with the String format."""

    def __init__(self, title):
        """Create the NonRequiredStringColumnType object."""
        super(NonRequiredStringColumnType, self).__init__(title, "string", " ")


class DateColumnType(TreeviewColumn):
    """Class to format columns with the Date format."""

    def __init__(self, title):
        """Create the DateColumnType object."""
        super(DateColumnType, self).__init__(title, "date", " ")


class PercentageColumnType(TreeviewColumn):
    """Class to format columns with the Percentage format."""

    def __init__(self, title):
        """Create the PercentageColumnType object."""
        super(PercentageColumnType, self).__init__(title, "percentage", " ")


class FloatColumnType(TreeviewColumn):
    """Class to format columns with the Float format."""

    def __init__(self, title):
        """Create the FloatColumnType object."""
        super(FloatColumnType, self).__init__(title, "float", "0.00")


class CurencyColumnType(TreeviewColumn):
    """Class to format columns with the Currency format."""

    def __init__(self, title):
        """Create the CurencyColumnType object."""
        super(CurencyColumnType, self).__init__(title, "currency", "0.00")
