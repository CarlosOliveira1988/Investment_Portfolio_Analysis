"""This file has classes to show windows for portfolio balancing purpose."""

from gui_lib.window import Window
from PyQt5 import QtWidgets

from balance_lib.balance_tabs import BalancingWindowTabs
from balance_lib.get_config import ConfigurationManager


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
        - RendaVariavel_df, RendaFixa_df, TesouroDireto_df: dataframes related
        to the opened positions in the portfolio
        - auto_show (True/False): flag to show window while creating the object
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

        # Set the window properties
        self.__setWindowProperties()

        # Show the window
        if auto_show:
            self.showMaximized()

    """Private methods."""

    def __setWindowProperties(self):
        spacing = Window.DEFAULT_BORDER_SIZE / 2
        internal_spacing = Window.DEFAULT_BORDER_SIZE

        # Create the grid object
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid.setSpacing(internal_spacing)
        self.grid.addWidget(self.TabGroup)

        # Set the grid layout
        self.setLayout(self.grid)

        # Set the title
        self.setWindowTitle("Balanceamento de Carteira")
