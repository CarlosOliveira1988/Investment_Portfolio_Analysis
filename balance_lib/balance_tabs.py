"""This file is useful to handle special tab panels portfolio balancing."""

from PyQt5 import QtWidgets

from balance_lib.balance_panels import AssetsTabPanel, GeneralTabPanel


class BalancingWindowTabs(QtWidgets.QTabWidget):
    """Class used to create special tabs."""

    def __init__(
        self,
        RendaVariavel_df,
        RendaFixa_df,
        TesouroDireto_df,
        ConfigurationManagerObj,
    ):
        """Create the BalancingWindowTabs object.

        Arguments:
        - RendaVariavel_df, RendaFixa_df, TesouroDireto_df: short and
        filtered dataframes exported by the 'PortfolioInvestment' class
        type, grouped per investment types:
          * RendaVariavel_df: ""Ações", "BDR", "ETF", "FII"
          * RendaFixa_df: "Prefixado", "CDI", "IPCA"
          * TesouroDireto_df: "Prefixado", "SELIC", "IPCA"
        - ConfigurationManagerObj: an object related to the
        'ConfigurationManager' class type
        """
        super().__init__()
        self.config = ConfigurationManagerObj

        # Control variable
        self.tab_list = []

        # General tab
        self.GeneralTabPanel, self.GeneralTabIndex = self.__addGeneralTab(
            RendaVariavel_df,
            RendaFixa_df,
            TesouroDireto_df,
        )

        # Assets tabs
        self.RVTabPanel, self.RVTabIndex = self.__addAssetsTab(
            RendaVariavel_df,
            self.config.RendaVariavel,
        )
        self.RFTabPanel, self.RFTabIndex = self.__addAssetsTab(
            RendaFixa_df,
            self.config.RendaFixa,
        )
        self.TDTabPanel, self.TDTabIndex = self.__addAssetsTab(
            TesouroDireto_df,
            self.config.TesouroDireto,
        )

        # Connect tab event
        self.currentChanged.connect(self.onChange)

    """Private methods."""

    def __addGeneralTab(
        self,
        RendaVariavel_df,
        RendaFixa_df,
        TesouroDireto_df,
    ):
        tab_panel = GeneralTabPanel(
            RendaVariavel_df.copy(),
            RendaFixa_df.copy(),
            TesouroDireto_df.copy(),
            self.config,
        )
        return self.__getTabPanelAndIndex(tab_panel)

    def __addAssetsTab(self, assets_df, InvestmentConfigObj):
        tab_panel = AssetsTabPanel(
            assets_df.copy(),
            InvestmentConfigObj,
            self.config.isDefaultConfigFile(),
        )
        return self.__getTabPanelAndIndex(tab_panel)

    def __getTabPanelAndIndex(self, tab_panel):
        tab_index = self.addTab(tab_panel.getTab(), tab_panel.getTabTitle())
        self.tab_list.append(tab_panel)
        return tab_panel, tab_index

    """Public methods."""

    def updateConfigurationValues(self):
        """Update configuration values from configuration file."""
        for tab in self.tab_list:
            tab.updateConfigurationValues()

    def onChange(self, index):
        """Onchange tab method to render the table columns."""
        for tab in self.tab_list:
            tab.resize()
