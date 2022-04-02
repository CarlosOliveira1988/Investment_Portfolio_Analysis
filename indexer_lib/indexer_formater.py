"""This file is useful to format the portfolio dataframe."""

from gui_lib.treeview.format_applier import EasyFormatter


class StackedIndexerFormater(EasyFormatter):
    """This class is useful to format Economic Indexers.

    Basically, here we manipulate the dataframe to define:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - data_frame: the portfolio pandas dataframe
    """

    def __init__(self, data_frame):
        """Create the StackedIndexerFormater object."""
        from indexer_lib.indexer_manager import StackedFormatConstants

        self.__StackedConstants = StackedFormatConstants()
        column_type_dict = {
            self.__StackedConstants.getYearTitle(): "s",
            self.__StackedConstants.getMonthTitle(): "s",
            self.__StackedConstants.getAdjustedDateTitle(): "0-0",
            self.__StackedConstants.getInterestTitle(): "s",
        }
        super().__init__(data_frame, column_type_dict)


class OriginalIndexerFormater(EasyFormatter):
    """This class is useful to format Economic Indexers.

     Basically, here we manipulate the dataframe to define:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - data_frame: the portfolio pandas dataframe
    """

    def __init__(self, data_frame):
        """Create the OriginalIndexerFormater object."""
        from indexer_lib.indexer_manager import OriginalFormatConstants

        self.__Original = OriginalFormatConstants()
        column_type_dict = {
            self.__Original.getYearTitle(): "s",
            self.__Original.getMonthsList()[0]: "%",
            self.__Original.getMonthsList()[1]: "%",
            self.__Original.getMonthsList()[2]: "%",
            self.__Original.getMonthsList()[3]: "%",
            self.__Original.getMonthsList()[4]: "%",
            self.__Original.getMonthsList()[5]: "%",
            self.__Original.getMonthsList()[6]: "%",
            self.__Original.getMonthsList()[7]: "%",
            self.__Original.getMonthsList()[8]: "%",
            self.__Original.getMonthsList()[9]: "%",
            self.__Original.getMonthsList()[10]: "%",
            self.__Original.getMonthsList()[11]: "%",
            self.__Original.getYearlyInterestRateTitle(): "%",
        }
        super().__init__(data_frame, column_type_dict)
