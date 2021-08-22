"""This is the main file of the project."""

from gui_lib.window import Window
from portfolio_widget import PortfolioViewerWidget


class MainWindow(Window):
    """Class used to create the Main Window of the project."""

    def __init__(self, portfolio_dataframe):
        """Create the MainWindow object."""
        super().__init__("Análise de Portfólio")
        self.PortfolioViewerWidget = PortfolioViewerWidget(
            self.getCentralWidget(),
            portfolio_dataframe,
        )

        # Window dimensions
        self.setFixedSize(
            self.PortfolioViewerWidget.getInternalWidth() + 25,
            self.PortfolioViewerWidget.getInternalHeight() + 25,
        )


if __name__ == "__main__":

    # Define the constants
    FILE_NAME = "\\PORTFOLIO_TEMPLATE.xlsx"
    FILE_SHEET = r"Extrato"

    # Create the application
    import sys

    from PyQt5 import QtWidgets

    from extrato import readOperations

    app = QtWidgets.QApplication(sys.argv)

    # Create the dataframe
    source_file_directory = sys.path[0]
    portolio_dataframe = readOperations(source_file_directory + FILE_NAME)

    # Create and shows the "MainWindow" object
    main = MainWindow(portolio_dataframe)
    main.show()

    # End the application when everything is closed
    sys.exit(app.exec_())
