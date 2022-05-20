"""This file is responsible to define the 'File' menu."""

import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from main_lib.menu_interfaces import MenuInterface


class FileMenu(MenuInterface):
    """FileMenu class."""

    def __init__(
        self,
        menu_bar,
        PortfolioViewerWidget,
        file_name,
        status_bar_function,
        close_function,
    ):
        """Create the FileMenu object."""
        super().__init__("&Arquivo", menu_bar)
        self.menu_bar = menu_bar
        self.PortfolioViewerWidget = PortfolioViewerWidget
        self.status_bar_function = status_bar_function
        self.close_function = close_function
        self.file_name = file_name

        # Create the submenus
        self.open = self.addSubmenu(
            "&Abrir Extrato",
            self.openFile,
        )
        self.exportGD = self.addSubmenu(
            "&Exportar Planilha Google Drive",
            self.exportGDFile,
        )
        self.exit = self.addSubmenu(
            "&Sair",
            self.exitApp,
        )

    def reopenFile(self):
        """Reopen the 'Extrato' spreadsheet."""
        if self.file_name:
            self.PortfolioViewerWidget.clearData()
            self.PortfolioViewerWidget.updateData(self.file_name)
            self.status_bar_function(self.file_name)

    def openFile(self):
        """Open the 'Extrato' spreadsheet."""
        file_name_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Selecione o arquivo XLSX relacionado ao portfolio",
            sys.path[0],
            "xlsx(*.xlsx)",
        )
        file_name = file_name_tuple[0]
        if ".xlsx" in file_name:
            self.file_name = file_name
            self.reopenFile()

    def exportGDFile(self):
        """Export the Google Drive spreadsheet."""
        try:
            self.PortfolioViewerWidget.exportGoogleDriveSheet()
            msg = "Planilha Google Drive exportada com sucesso.\n\n"
            QMessageBox.information(
                self,
                "Análise de Portfólio",
                msg,
                QMessageBox.Ok,
            )
        except AttributeError:
            msg = "Não foi possível exportar a planilha Google Drive."
            msg += "\n\nPlanilha extrato inválida."
            QMessageBox.warning(
                self,
                "Análise de Portfólio",
                msg,
                QMessageBox.Ok,
            )
        except PermissionError:
            msg = "Não foi possível exportar a planilha Google Drive."
            msg += "\n\nVerifique se o arquivo não está aberto."
            QMessageBox.warning(
                self,
                "Análise de Portfólio",
                msg,
                QMessageBox.Ok,
            )

    def exitApp(self):
        """Close the application."""
        self.close_function()
