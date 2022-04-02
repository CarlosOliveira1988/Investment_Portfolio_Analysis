"""This file is useful to format the portfolio dataframe."""


from gui_lib.treeview.format_applier import EasyFormatter


class PortfolioFormater(EasyFormatter):
    """This class is useful to format Portfolio DataFrames.

    Basically, here we manipulate the dataframe to define:
    - the columns order
    - the columns types
    - the number of columns

    Arguments:
    - portfolio_data_frame: the portfolio pandas dataframe
    """

    def __init__(self, portfolio_data_frame):
        """Create the PortfolioFormater object."""
        column_type_dict = {
            "Mercado": "s",
            "Ticker": "s",
            "Operação": "s",
            "Data": "0-0",
            "Rentabilidade Contratada": "%",
            "Indexador": "ns",
            "Vencimento": "0-0",
            "Quantidade": "0.0",
            "Preço Unitário": "$",
            "Preço Total": "$",
            "Taxas": "$",
            "IR": "$",
            "Dividendos": "$",
            "JCP": "$",
            "Custo Total": "$",
            "Notas": "ns",
        }
        super().__init__(portfolio_data_frame, column_type_dict)


class VariableIncomesFormater(EasyFormatter):
    """This class is useful to format Portfolio DataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - portfolio_data_frame: the portfolio pandas dataframe
    """

    def __init__(self, portfolio_data_frame):
        """Create the VariableIncomesFormater object."""
        column_type_dict = {
            "Mercado": "s",
            "Ticker": "s",
            "Dividend-Yield Ajustado": "%",
            "Data Inicial": "0-0",
            "Quantidade": "0.0",
            "Preço médio": "$",
            "Preço médio+taxas": "$",
            "Cotação": "$",
            "Preço pago": "$",
            "Preço mercado": "$",
            "Mercado-pago": "$",
            "Mercado-pago(%)": "%",
            "Vendas parciais": "$",
            "Taxas Adicionais": "$",
            "IR": "$",
            "Dividendos": "$",
            "JCP": "$",
            "Líquido parcial": "$",
            "Líquido parcial(%)": "%",
            "Porcentagem carteira": "%",
        }
        super().__init__(portfolio_data_frame, column_type_dict)


class TreasuriesFormater(EasyFormatter):
    """This class is useful to format Portfolio DataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - portfolio_data_frame: the portfolio pandas dataframe
    """

    def __init__(self, portfolio_data_frame):
        """Create the TreasuriesFormater object."""
        column_type_dict = {
            "Ticker": "s",
            "Indexador": "s",
            "Rentabilidade-média Contratada": "%",
            "Data Inicial": "0-0",
            "Quantidade": "0.0",
            "Preço médio": "$",
            "Preço médio+taxas": "$",
            "Cotação": "$",
            "Preço pago": "$",
            "Preço mercado": "$",
            "Mercado-pago": "$",
            "Mercado-pago(%)": "%",
            "Vendas parciais": "$",
            "Taxas Adicionais": "$",
            "IR": "$",
            "Dividendos": "$",
            "JCP": "$",
            "Líquido parcial": "$",
            "Líquido parcial(%)": "%",
            "Porcentagem carteira": "%",
        }
        super().__init__(portfolio_data_frame, column_type_dict)


class FixedIncomesFormater(EasyFormatter):
    """This class is useful to format Portfolio DataFrames.

    Basically, here we manipulate the dataframe to define:

    Arguments:
    - portfolio_data_frame: the portfolio pandas dataframe
    """

    def __init__(self, portfolio_data_frame):
        """Create the FixedIncomesFormater object."""
        column_type_dict = {
            "Ticker": "s",
            "Indexador": "s",
            "Rentabilidade-média Contratada": "%",
            "Data Inicial": "0-0",
            "Quantidade": "0.0",
            "Preço médio": "$",
            "Preço médio+taxas": "$",
            "Cotação": "$",
            "Preço pago": "$",
            "Preço mercado": "$",
            "Mercado-pago": "$",
            "Mercado-pago(%)": "%",
            "Vendas parciais": "$",
            "Taxas Adicionais": "$",
            "IR": "$",
            "Dividendos": "$",
            "JCP": "$",
            "Líquido parcial": "$",
            "Líquido parcial(%)": "%",
            "Porcentagem carteira": "%",
        }
        super().__init__(portfolio_data_frame, column_type_dict)
