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
        self.__initTreeviewData()

    def __initTreeviewData(self):
        self.Treeview = self.PortfolioViewerWidget.getTreeview()
        self.__insertTreeviewParentLines()
        self.__insertTreeviewChildrenLines()
        self.Treeview.expandParentLines()
        self.Treeview.resizeColumnsToContents()
        self.Treeview.collapseParentLines()

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
    FILE_NAME = '\PORTFOLIO_TEMPLATE.xlsx'
    FILE_SHEET = r'Extrato'

    # Creates the application
    import sys
    from PyQt5 import QtWidgets
    from extrato import readOperations
    app = QtWidgets.QApplication(sys.argv)

    # Get the path of the main folder 'Investment_Portfolio_Analysis'
    def getMainPath():
        main_file_path = None
        file_path_list = sys.path
        for path_item in file_path_list:
            if '\Investment_Portfolio_Analysis' in path_item:
                main_file_path = path_item
        return main_file_path

    # Creates the dataframe
    source_file_directory = getMainPath()
    portolio_dataframe = readOperations(source_file_directory + FILE_NAME)

    # Creates and shows the "MainWindow" object
    main = MainWindow(portolio_dataframe)
    main.showMaximized()

    # Ends the application when everything is closed
    sys.exit(app.exec_())
