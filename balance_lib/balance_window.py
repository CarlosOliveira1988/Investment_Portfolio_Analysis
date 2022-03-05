"""This file has classes to show windows for portfolio balancing purpose."""

from gui_lib.pushbutton import StandardPushButton
from gui_lib.window import Window
from PyQt5 import QtCore, QtWidgets

from balance_lib.balance_tabs import BalancingWindowTabs
from balance_lib.get_config import ConfigurationManager


class UpdateConfigurationButton(QtWidgets.QPushButton):
    """Button used to reload the configuration values from file."""

    def __init__(self, onClickMethod):
        """Create the UpdateConfigurationButton object.

        Arguments:
        - onClickMethod: any method to be called when clicking in the button
        """
        super().__init__("ATUALIZAR\nCONFIGURAÇÕES")
        self.setFixedSize(
            QtCore.QSize(
                StandardPushButton.DEFAULT_WIDTH,
                StandardPushButton.DEFAULT_HEIGHT * 2,
            )
        )
        self.clicked.connect(onClickMethod)


class BalancingWindow(QtWidgets.QWidget):
    """Window class used to show Balancing Portfolio frames."""

    def __init__(
        self,
        RendaVariavel_df,
        RendaFixa_df,
        TesouroDireto_df,
        extrato_path,
        auto_show=True,
    ):
        """Create the BalancingWindow object.

        Arguments:
        - RendaVariavel_df, RendaFixa_df, TesouroDireto_df: short and
        filtered dataframes exported by the 'PortfolioInvestment' class
        type, grouped per investment types:
          * RendaVariavel_df: ""Ações", "BDR", "ETF", "FII"
          * RendaFixa_df: "Prefixado", "CDI", "IPCA"
          * TesouroDireto_df: "Prefixado", "SELIC", "IPCA"
        - extrato_path: a string related to the directory where the extrato
        spreadsheet is located
        - auto_show (True/False): flag to show the window while creating
        the object
        """
        super().__init__()

        # Configuration manager
        self.config = ConfigurationManager(extrato_path)

        # Tab group
        self.TabGroup = BalancingWindowTabs(
            RendaVariavel_df,
            RendaFixa_df,
            TesouroDireto_df,
            self.config,
        )

        # Update configuration button
        self.ConfigButton = UpdateConfigurationButton(self.updateConfig)

        # Set the window properties
        self.__setWindowProperties()

        # Show the window
        if auto_show:
            self.showMaximized()

    """Private methods."""

    def __setWindowProperties(self):
        spacing = Window.DEFAULT_BORDER_SIZE / 2

        # Create the grid object
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid.setSpacing(spacing)
        self.grid.addWidget(self.TabGroup)
        self.grid.addWidget(
            self.ConfigButton, 1, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # Set the grid layout
        self.setLayout(self.grid)

        # Set the title
        self.setWindowTitle("Balanceamento de Carteira")

    """Public methods."""

    def updateConfig(self):
        """Update configuration values from configuration file."""
        self.TabGroup.updateConfigurationValues()
