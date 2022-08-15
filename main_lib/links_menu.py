"""This file is responsible to define the 'Links' menu."""

import webbrowser

from main_lib.menu_interfaces import MenuInterface


class LinksMenu(MenuInterface):
    """LinksMenu class."""

    def __init__(self, menu_bar):
        """Create the LinksMenu object."""
        super().__init__("&Links Externos", menu_bar)
        self.menu_bar = menu_bar

        # Create the submenus
        self.focus = self.addSubmenu(
            "&Relatório Focus",
            self.focusReportLink,
        )
        self.fixedIncome = self.addSubmenu(
            "&Simulador de Renda Fixa",
            self.fixedIncomeLink,
        )
        self.profitability = self.addSubmenu(
            "&Simulador de Rentabilidade",
            self.profitabilityLink,
        )
        self.extratoHistory = self.addSubmenu(
            "&Histórico de Extrato",
            self.extratoHistoryLink,
        )

    def focusReportLink(self):
        """Open the 'Relatorio Focus' weblink."""
        webbrowser.open(r"https://www.bcb.gov.br/publicacoes/focus")

    def fixedIncomeLink(self):
        """Open a weblink related to 'Renda Fixa'."""
        webbrowser.open(r"https://rendafixa.herokuapp.com")

    def profitabilityLink(self):
        """Open a weblink related to 'Rentabilidade'."""
        webbrowser.open(r"http://rendafixa.herokuapp.com/rentabilidade")

    def extratoHistoryLink(self):
        """Open a weblink related to 'Extrato History'."""
        webbrowser.open(
            r"https://carlosoliveira1988-portfoliogui-home-i621k2.streamlitapp.com/"
        )
