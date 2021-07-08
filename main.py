from window import Window
from portolio_widget import PortfolioViewerWidget
from portfolio_viewer_manager import PortfolioViewerManager


class MainWindow(Window):
    """ 
    This is the main class of the project, where all GUI components are placed.
    """
    def __init__(self, portolio_dataframe):
        super().__init__('Investment Portfolio Analysis')
        self.PortfolioViewerManager = PortfolioViewerManager(portolio_dataframe)
        self.PortfolioViewerWidget = PortfolioViewerWidget(self.getCentralWidget(), self.PortfolioViewerManager.getColumnsTitleList())
        self.Treeview = self.PortfolioViewerWidget.getTreeview()
        self.__insertTreeviewParentLines()
        self.__insertTreeviewChildrenLines()

    def __insertTreeviewParentLines(self):
        self.TreeviewParentLinesDictionary = {}
        non_duplicated_market_list = self.PortfolioViewerManager.getColumnNonDuplicatedValuesList('Mercado')
        for market in non_duplicated_market_list:
            parent_line = self.Treeview.insertParentLineItem(market)
            self.TreeviewParentLinesDictionary[market] = parent_line

    def __insertTreeviewChildrenLines(self):
        for selected_market, market_parent_line in self.TreeviewParentLinesDictionary.items():
            df_per_market = self.PortfolioViewerManager.getCustomTable(market=selected_market)
            for line_data_row in df_per_market.itertuples(index=False):
                line_data_row_list = list(line_data_row)
                line_data_row_list[0] = ' '
                self.Treeview.insertChildrenLineData(market_parent_line, line_data_row_list)


if __name__ == "__main__":

    # Define the constants
    SOURCE_FILE_DIRECTORY = r'D:\Dudu\Finanças\Investimentos\Mercado Financeiro\Investment_Portfolio_Analysis'
    FILE_NAME = r'\PORTFOLIO_TEMPLATE.xlsx'
    FILE_SHEET = r'Extrato'
    FILE = SOURCE_FILE_DIRECTORY + FILE_NAME

    # Creates the application
    from PyQt5 import QtWidgets
    import sys
    import pandas as pd
    app = QtWidgets.QApplication(sys.argv)

    # Creates the dataframe
    portolio_dataframe = pd.read_excel(FILE, sheet_name=FILE_SHEET)

    # Creates and shows the "MainWindow" object
    main = MainWindow(portolio_dataframe)
    main.showMaximized()

    # Ends the application when everything is closed
    sys.exit(app.exec_())
