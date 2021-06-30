import pandas as pd

from data_viewer import DataViewer
from portfolio_formater import PortfolioFormater


SOURCE_FILE_DIRECTORY = r'D:\Dudu\Finanças\Investimentos\Mercado Financeiro'
FILE_NAME = r'\Poupanca_one_tab.xlsx'
FILE_SHEET = r'Saldo Custódia RICO'

FILE = SOURCE_FILE_DIRECTORY + FILE_NAME


class Portfolio:
    def __init__(self, PortolioDataFrame):
        self.PortfolioFormater = PortfolioFormater(PortolioDataFrame)
        self.FormatedPortolioDataFrame = self.PortfolioFormater.getFormatedPortolioDataFrame()

    """
    Public methods
    """
    def getColumnsTitleList(self):
        return self.PortfolioFormater.getColumnsTitleList()

    def getColumnNonDuplicatedValuesList(self, column_header):
        column_list = list(self.FormatedPortolioDataFrame[column_header])
        column_list = list(set(column_list))
        if 'NA' in column_list:
            column_list.remove('NA')
        return column_list
    
    def getCustomTable (self, ticker='all', market='all', dueDate='NA', profitability='NA', index='all', operation='all'):
        if ticker != 'all':
            table = self.FormatedPortolioDataFrame[self.FormatedPortolioDataFrame['Ticker'] == ticker]
        if market != 'all':
            table = self.FormatedPortolioDataFrame[self.FormatedPortolioDataFrame['Mercado'] == market]
        if dueDate != 'NA':
            table = self.FormatedPortolioDataFrame[self.FormatedPortolioDataFrame['Vencimento'] == dueDate]
        if profitability != 'NA':
            table = self.FormatedPortolioDataFrame[self.FormatedPortolioDataFrame['Rentabilidade Contratada'] == dueDate]
        if index != 'all':
            table = self.FormatedPortolioDataFrame[self.FormatedPortolioDataFrame['Indexador'] == index]
        if operation != 'all':
            table = self.FormatedPortolioDataFrame[self.FormatedPortolioDataFrame['Operação'] == operation]
        return table


# Example of how to use the "Portolio" class
if __name__ == "__main__":
    # Creates the application
    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Creates the dataframe
    portolio_dataframe = pd.read_excel(FILE, sheet_name=FILE_SHEET)

    # Creates the "Portolio" object
    my_portfolio = Portfolio(portolio_dataframe)

    # Creates the "DataViewer" object
    data_viewer = DataViewer('Portfolio Analysis', my_portfolio.getColumnsTitleList())

    # Insert the parent lines in the "DataViewer" object
    parent_line_dict = {}
    non_duplicated_market_list = my_portfolio.getColumnNonDuplicatedValuesList('Mercado')
    for market in non_duplicated_market_list:
        parent_line = data_viewer.DataViewerTable.insertParentLineItem(market)
        parent_line_dict[market] = parent_line

    # Insert the children lines in the "DataViewer" object
    for selected_market, market_parent_line in parent_line_dict.items():
        df_per_market = my_portfolio.getCustomTable(market=selected_market)
        for line_data_row in df_per_market.itertuples(index=False):
            line_data_row_list = list(line_data_row)
            line_data_row_list[0] = ' '
            data_viewer.DataViewerTable.insertChildrenLineData(market_parent_line, line_data_row_list)

    # Shows the "DataViewer" object
    data_viewer.showMaximized()

    # Ends the application when everything is closed
    sys.exit(app.exec_())
