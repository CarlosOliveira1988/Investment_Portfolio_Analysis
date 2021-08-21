import locale
from datetime import datetime

import pandas as pd


class TreeviewValueFormat:
    """
    A collection of methods to format values as follows:
    - Date: 2021/06/27
    - Float: 1.00
    - Percentage: 1.00%
    - Currency: R$ 1,00
    - String: String
    """

    def setDateFormat(date_string):
        if isinstance(date_string, pd.Timestamp) or isinstance(date_string, datetime):
            return str(date_string.strftime("%Y/%m/%d"))
        else:
            return date_string

    def setDateTimeFormat(date_string):
        if isinstance(date_string, pd.Timestamp) or isinstance(date_string, datetime):
            return str(date_string.strftime("%Y/%m/%d %H:%M:%S"))
        else:
            return date_string

    def setFloatFormat(float_value):
        if isinstance(float_value, float) or isinstance(float_value, int):
            return "{0:.2f}".format(float(float_value))
        else:
            return float_value

    def setPercentageFormat(percentage_value):
        if isinstance(percentage_value, float) or isinstance(percentage_value, int):
            return "{0:.2f}%".format(float(percentage_value) * 100)
        else:
            return percentage_value

    def setCurrencyFormat(currency_value):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        if isinstance(currency_value, float) or isinstance(currency_value, int):
            return locale.currency(float(currency_value), grouping=True)
        else:
            return currency_value

    def setStringFormat(string_value):
        return string_value


class TreeviewDataframeFormat:
    """
    A collection of methods to format data frame columns as follows:
    - Date: 2021-06-27
    - Float: 1.00
    - Percentage: 1.00%
    - Currency: R$ 1,00
    - String: String
    """

    def setDateFormat(data_frame, date_column):
        date_list = [
            TreeviewValueFormat.setDateFormat(date_string)
            for date_string in list(data_frame[date_column])
        ]
        data_frame[date_column] = date_list

    def setFloatFormat(data_frame, float_column):
        float_list = [
            TreeviewValueFormat.setFloatFormat(float_value)
            for float_value in list(data_frame[float_column])
        ]
        data_frame[float_column] = float_list

    def setPercentageFormat(data_frame, percentage_column):
        percentage_list = [
            TreeviewValueFormat.setPercentageFormat(percentage_value)
            for percentage_value in list(data_frame[percentage_column])
        ]
        data_frame[percentage_column] = percentage_list

    def setCurrencyFormat(data_frame, currency_column):
        currency_list = [
            TreeviewValueFormat.setCurrencyFormat(currency_value)
            for currency_value in list(data_frame[currency_column])
        ]
        data_frame[currency_column] = currency_list

    def setStringFormat(data_frame, string_column):
        string_list = [
            TreeviewValueFormat.setStringFormat(string_value)
            for string_value in list(data_frame[string_column])
        ]
        data_frame[string_column] = string_list


class TreeviewColumn:
    """
    A collection of methods and attributes to format data frame columns as follows:
    - Date: 2021-06-27
    - Float: 1.00
    - Percentage: 1.00%
    - Currency: R$ 1,00
    - String: String

    Arguments:
    - title: the column title
    - format_type: the column format (date / float / percentage / currency / string)
    - na_value: the string used to fill na values (example: 'R$ 0.00')
    """

    def __init__(self, title, format_type, na_value):
        self.Title = title
        self.FormatType = format_type
        self.NaValue = na_value

    def formatValue(self, value):
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
        data_frame[self.Title].fillna(value=self.NaValue, inplace=True)

    def getTitle(self):
        return self.Title


class RequiredStringColumnType(TreeviewColumn):
    def __init__(self, title):
        super(RequiredStringColumnType, self).__init__(title, "string", "NA")


class NonRequiredStringColumnType(TreeviewColumn):
    def __init__(self, title):
        super(NonRequiredStringColumnType, self).__init__(title, "string", " ")


class DateColumnType(TreeviewColumn):
    def __init__(self, title):
        super(DateColumnType, self).__init__(title, "date", " ")


class PercentageColumnType(TreeviewColumn):
    def __init__(self, title):
        super(PercentageColumnType, self).__init__(title, "percentage", " ")


class FloatColumnType(TreeviewColumn):
    def __init__(self, title):
        super(FloatColumnType, self).__init__(title, "float", "0.00")


class CurencyColumnType(TreeviewColumn):
    def __init__(self, title):
        super(CurencyColumnType, self).__init__(title, "currency", "0.00")
