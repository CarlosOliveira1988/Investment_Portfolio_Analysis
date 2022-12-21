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
            "Mercado": "s",
            "Valor atual": "$",
            "Variação no dia": "%",
            "Min. no mês": "$",
            "Máx. no mês": "$",
            "Variação no mês": "%",
            "Min. 52 semanas": "$",
            "Máx. 52 semanas": "$",
            "Variação 12 meses": "%",
            "Dividend yield": "%",
            "Dividendos 12 meses": "$",
            "P/L": "0.0",
            "P/VP": "0.0",
            "VPA": "$",
            "LPA": "$",
        }
        super().__init__(dataframe, column_type_dict)
