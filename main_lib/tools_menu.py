"""This file is responsible to define the 'Tools' menu."""

from balance_lib.balance_window import BalancingWindow
from indexer_lib.economic_indexers_window import EconomicIndexerWindow
from valuation_lib.valuation_window import ValuationWindow

from main_lib.menu_interfaces import MenuInterface


class ToolsMenu(MenuInterface):
    """ToolsMenu class."""

    def __init__(self, menu_bar, PortfolioViewerWidget):
        """Create the ToolsMenu object."""
        super().__init__("&Ferramentas", menu_bar)
        self.menu_bar = menu_bar
        self.PortfolioViewerWidget = PortfolioViewerWidget

        # Variables for External Windows
        self.EconomicIndexerWindow = None
        self.ValuationWindow = None
        self.BalancingWindow = None

        # Create the submenus
        self.indexers = self.addSubmenu(
            "&Indicadores Econômicos",
            self.indexerWin,
        )
        self.valuation = self.addSubmenu(
            "&Indicadores Fundamentalistas",
            self.valuationWin,
        )
        self.balancing = self.addSubmenu(
            "&Balanceamento de Carteira",
            self.balancingWin,
        )

    def indexerWin(self):
        """Launch the EconomicIndexer app."""
        self.EconomicIndexerWindow = EconomicIndexerWindow()

    def valuationWin(self):
        """Launch the Valuation app."""
        self.ValuationWindow = ValuationWindow()

    def balancingWin(self):
        """Launch the Portfolio Balancing app."""
        investment = self.PortfolioViewerWidget.getPortfolioInvestmentObject()
        extrato_path = self.PortfolioViewerWidget.getExtratoPath()
        self.BalancingWindow = BalancingWindow(
            investment.currentPortfolio(),
            investment.currentRendaFixa(),
            investment.currentTesouroDireto(),
            extrato_path,
        )
