"""This file has classes to show windows for portfolio balancing purpose."""

import subprocess

from gui_lib.pushbutton import StandardPushButton
from gui_lib.window import Window
from PyQt5 import QtCore, QtWidgets

from balance_lib.balance_tabs import BalancingWindowTabs
from balance_lib.get_config import ConfigurationManager


class Button(QtWidgets.QPushButton):
    """Button used to handle configuration files."""

    def __init__(self, title, onClickMethod):
        """Create the Button object.

        Arguments:
        - title: the text shown on the button
        - onClickMethod: any method to be called when clicking in the button
        """
        super().__init__(title)
        self.setFixedSize(
            QtCore.QSize(
                StandardPushButton.DEFAULT_WIDTH,
                StandardPushButton.DEFAULT_HEIGHT * 2,
            )
        )
        self.clicked.connect(onClickMethod)


class UpdateConfigurationButton(Button):
    """Button used to reload the configuration values from file."""

    def __init__(self, onClickMethod):
        """Create the UpdateConfigurationButton object."""
        super().__init__("ATUALIZAR\nCONFIGURAÇÕES", onClickMethod)


class EditConfigurationButton(Button):
    """Button used to edit the configuration file.

    Basically, it will try to open the Notepad++ ou Notepad.
    """

    def __init__(self, onClickMethod):
        """Create the EditConfigurationButton object."""
        super().__init__("EDITAR\nCONFIGURAÇÕES", onClickMethod)


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

        # Buttons
        self.ConfigButton = UpdateConfigurationButton(self.updateConfig)
        self.EditButton = EditConfigurationButton(self.editConfig)

        # Set the window properties
        self.__setWindowProperties()

        # Show the window
        if auto_show:
            self.showMaximized()

    """Private methods."""

    def __setWindowProperties(self):
        spacing = Window.DEFAULT_BORDER_SIZE / 2

        # Create the button grid object
        self.ButtonsWidget = QtWidgets.QWidget()
        self.ButtonGrid = QtWidgets.QHBoxLayout()
        self.ButtonGrid.setSpacing(spacing)
        self.ButtonGrid.addWidget(self.ConfigButton)
        self.ButtonGrid.addWidget(self.EditButton)
        self.ButtonsWidget.setLayout(self.ButtonGrid)

        # Create the grid object
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(spacing, spacing, spacing, spacing)
        self.grid.setSpacing(spacing)
        self.grid.addWidget(self.TabGroup)
        self.grid.addWidget(
            self.ButtonsWidget, 1, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # Set the grid layout
        self.setLayout(self.grid)

        # Set the title
        self.setWindowTitle("Balanceamento de Carteira")

    """Public methods."""

    def updateConfig(self):
        """Update configuration values from configuration file."""
        self.TabGroup.updateConfigurationValues()

    def editConfig(self):
        """Open the Notepad, then the user may edit the file."""
        subprocess.Popen(["notepad.exe", self.config.getConfigFile()])
