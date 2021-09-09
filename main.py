"""This is the main file of the project."""

from PyQt5 import QtWidgets

from portfolio_lib.portfolio_widget import PortfolioViewerWidget


class MainWindow(QtWidgets.QWidget):
    """Class used to create the Main Window of the project."""

    def __init__(self, file):
        """Create the MainWindow object."""
        super().__init__()
        self.setWindowTitle("Análise de Portfólio")

        # Grid layout manager
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        # Portfolio widget
        self.PortfolioViewerWidget = PortfolioViewerWidget(file)
        grid.addWidget(self.PortfolioViewerWidget)


if __name__ == "__main__":

    import sys

    SOURCE_FILE_DIRECTORY = sys.path[0] + "\\portfolio_lib"
    FILE_NAME = r"\PORTFOLIO_TEMPLATE.xlsx"

    # SOURCE_FILE_DIRECTORY = r"D:\Dudu\Finanças\Investimentos\Mercado Financeiro"
    # FILE_NAME = r"\Poupanca_one_tab.xlsx"

    # SOURCE_FILE_DIRECTORY = r"C:\Users\Fred\Documents\GitHub\Investment_Portfolio_Analysis"
    # FILE_NAME = r"\PORTFOLIO_TEMPLATE.xlsx"
    # FILE_NAME = r"\Extrato_Fred.xlsx"

    FILE = SOURCE_FILE_DIRECTORY + FILE_NAME

    # Create the application
    import sys

    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)

    # File directory
    source_file_directory = sys.path[0]

    # Create and shows the "MainWindow" object
    main = MainWindow(FILE)
    main.showMaximized()

    # End the application when everything is closed
    sys.exit(app.exec_())
