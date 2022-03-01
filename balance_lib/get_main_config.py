"""File used to get 'main' configuration from 'investimentos.ini' file."""

from balance_lib.get_config_interfaces import (
    InvestmentConfig,
    InvestmentConfigInterface,
)


class ClasseDeInvestimento(InvestmentConfig):
    """Handle the 'ClasseDeInvestimento' tag in configuration file."""

    def __init__(self, config_file):
        """Create the ClasseDeInvestimento object."""
        super().__init__(
            "ClasseDeInvestimento",
            "Classe de Investimento",
            ["RendaVariavel", "RendaFixa", "TesouroDireto"],
            ["Renda Variável", "Renda Fixa", "Tesouro Direto"],
            "Mercado",
            config_file,
        )


class RendaVariavel(InvestmentConfigInterface):
    """Handle the 'RendaVariavel' tag in configuration file."""

    def __init__(self, config_file):
        """Create the RendaVariavel object."""
        super().__init__(
            "RendaVariavel",
            "Renda Variável",
            ["Acoes", "BDR", "FII", "ETF"],
            ["Ações", "BDR", "FII", "ETF"],
            "Mercado",
            config_file,
        )


class RendaFixa(InvestmentConfigInterface):
    """Handle the 'RendaFixa' tag in configuration file."""

    def __init__(self, config_file):
        """Create the RendaFixa object."""
        super().__init__(
            "RendaFixa",
            "Renda Fixa",
            ["PREFIXADO", "CDI", "IPCA"],
            ["PREFIXADO", "CDI", "IPCA"],
            "Indexador",
            config_file,
        )


class TesouroDireto(InvestmentConfigInterface):
    """Handle the 'TesouroDireto' tag in configuration file."""

    def __init__(self, config_file):
        """Create the TesouroDireto object."""
        super().__init__(
            "TesouroDireto",
            "Tesouro Direto",
            ["PREFIXADO", "SELIC", "IPCA"],
            ["PREFIXADO", "SELIC", "IPCA"],
            "Indexador",
            config_file,
        )
