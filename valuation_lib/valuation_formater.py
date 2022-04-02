"""This file has methods to format valuation tables."""

from gui_lib.treeview.format_applier import EasyFormatter


class FundamentalAnalysisFormater(EasyFormatter):
    """This class is useful to format fundamentalist dataFrames.

    The following attributes are controlled by this class:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - dataframe: the fundamentalist pandas dataframe
    """

    def __init__(self, dataframe):
        """Create the FundamentalAnalysisFormater object."""
        column_type_dict = {
            "Ticker": "s",
            "Setor": "s",
            "Preço atual": "$",
            "VPA": "$",
            "LPA": "$",
            "P/L": "0.0",
            "P/VPA": "0.0",
            "Dividend Yield": "%",
            "Dividendos 12-meses": "$",
            "Data ex-dividendos": "0-0",
            "Data último-dividendo": "0-0",
            "Data último-split": "0-0",
        }
        super().__init__(dataframe, column_type_dict)
