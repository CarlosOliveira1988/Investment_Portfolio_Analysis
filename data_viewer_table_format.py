import pandas as pd
import locale


class DataViewerValueFormat:
    """
    A collection of methods to format values as follows:
    - Date: 2021/06/27
    - Float: 1.00
    - Percentage: 1.00%
    - Currency: R$ 1,00
    - String: String
    """
    def setDateFormat(date_string):
        if isinstance(date_string, pd.Timestamp):
            return str(date_string.strftime("%Y/%m/%d"))
        else:
            return date_string

    def setFloatFormat(float_value):
        if isinstance(float_value, float):
            return '{0:.2f}'.format(float_value)
        else:
            return float_value

    def setPercentageFormat(percentage_value):
        if isinstance(percentage_value, float):
            return '{0:.2f}%'.format(percentage_value*100)
        else:
            return percentage_value

    def setCurrencyFormat(currency_value):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        if isinstance(currency_value, float):
            return locale.currency(currency_value, grouping=True)
        else:
            return currency_value

    def setStringFormat(string_value):
        return string_value


class DataViewerDataFrameFormat:
    """
    A collection of methods to format data frame columns as follows:
    - Date: 2021-06-27
    - Float: 1.00
    - Percentage: 1.00%
    - Currency: R$ 1,00
    - String: String
    """
    def setDateFormat(data_frame, date_column):
        date_list = [DataViewerValueFormat.setDateFormat(date_string) for date_string in list(data_frame[date_column])]
        data_frame[date_column] = date_list

    def setFloatFormat(data_frame, float_column):
        float_list = [DataViewerValueFormat.setFloatFormat(float_value) for float_value in list(data_frame[float_column])]
        data_frame[float_column] = float_list

    def setPercentageFormat(data_frame, percentage_column):
        percentage_list = [DataViewerValueFormat.setPercentageFormat(percentage_value) for percentage_value in list(data_frame[percentage_column])]
        data_frame[percentage_column] = percentage_list

    def setCurrencyFormat(data_frame, currency_column):
        currency_list = [DataViewerValueFormat.setCurrencyFormat(currency_value) for currency_value in list(data_frame[currency_column])]
        data_frame[currency_column] = currency_list

    def setStringFormat(data_frame, string_column):
        string_list = [DataViewerValueFormat.setStringFormat(string_value) for string_value in list(data_frame[string_column])]
        data_frame[string_column] = string_list


class DataViewerTableColumn:
    def __init__(self, title, format_type, na_value):
        self.Title = title
        self.FormatType = format_type
        self.NaValue = na_value

    def formatValue(self, value):
        if self.FormatType == 'date':
            return DataViewerValueFormat.setDateFormat(value)
        elif self.FormatType == 'float':
            return DataViewerValueFormat.setFloatFormat(value)
        elif self.FormatType == 'percentage':
            return DataViewerValueFormat.setPercentageFormat(value)
        elif self.FormatType == 'currency':
            return DataViewerValueFormat.setCurrencyFormat(value)
        elif self.FormatType == 'string':
            return DataViewerValueFormat.setStringFormat(value)

    def formatDataFrameColumnValues(self, data_frame):
        if self.FormatType == 'date':
            DataViewerDataFrameFormat.setDateFormat(data_frame, self.Title)
        elif self.FormatType == 'float':
            DataViewerDataFrameFormat.setFloatFormat(data_frame, self.Title)
        elif self.FormatType == 'percentage':
            DataViewerDataFrameFormat.setPercentageFormat(data_frame, self.Title)
        elif self.FormatType == 'currency':
            DataViewerDataFrameFormat.setCurrencyFormat(data_frame, self.Title)
        elif self.FormatType == 'string':
            DataViewerDataFrameFormat.setStringFormat(data_frame, self.Title)

    def fillNaDataFrameColumnValues(self, data_frame):
        data_frame[self.Title].fillna(value=self.NaValue, inplace=True)
    
    def getTitle(self):
        return self.Title


class RequiredStringColumnType(DataViewerTableColumn):
    def __init__(self, title):
        super(RequiredStringColumnType, self).__init__(title, 'string', 'NA')


class NonRequiredStringColumnType(DataViewerTableColumn):
    def __init__(self, title):
        super(NonRequiredStringColumnType, self).__init__(title, 'string', ' ')


class DateColumnType(DataViewerTableColumn):
    def __init__(self, title):
        super(DateColumnType, self).__init__(title, 'date', ' ')


class PercentageColumnType(DataViewerTableColumn):
    def __init__(self, title):
        super(PercentageColumnType, self).__init__(title, 'percentage', ' ')


class FloatColumnType(DataViewerTableColumn):
    def __init__(self, title):
        super(FloatColumnType, self).__init__(title, 'float', '0.00')


class CurencyColumnType(DataViewerTableColumn):
    def __init__(self, title):
        super(CurencyColumnType, self).__init__(title, 'currency', '0.00')
