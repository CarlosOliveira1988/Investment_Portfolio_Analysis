from data_viewer_window import DataViewerWindow
from data_viewer_table import DataViewerTable


class DataViewerPandas(DataViewerTable):
    """ 
    This class provides methods and attributes to show Pandas DataFrames in a table.

    Arguments:
    - DataViewerWindow: the 'DataViewerWindow' window object
    - PandasDataFrame: the pandas dataframe
    """
    def __init__(self, DataViewerWindow, PandasDataFrame):
        self.PandasDataFrame = PandasDataFrame
        super().__init__(DataViewerWindow, list(self.PandasDataFrame))

    def showPandas(self):
        for line_data_row in self.PandasDataFrame.itertuples(index=False):
            line_data_row_list = list(line_data_row)
            items_list = self.convertValuesListToItemsList(line_data_row_list)
            self.insertParentLine(items_list)


# Example of how to use the "DataViewerPandas" class
if __name__ == "__main__":

    # Define the constants
    SOURCE_FILE_DIRECTORY = r'D:\Dudu\Finanças\Investimentos\Mercado Financeiro'
    FILE_NAME = r'\Poupanca_one_tab.xlsx'
    FILE_SHEET = r'Saldo Custódia RICO'
    FILE = SOURCE_FILE_DIRECTORY + FILE_NAME

    # Creates the application
    import sys
    from PyQt5 import QtWidgets
    from extrato import readOperations
    app = QtWidgets.QApplication(sys.argv)

    # Creates the data viewer window
    data_viewer_window = DataViewerWindow('Testing Pandas Data Viewer')

    # Creates the pandas dataframe
    pandas_dataframe = readOperations(FILE)

    # Creates the pandas data viewer
    pandas_data_viewer = DataViewerPandas(data_viewer_window, pandas_dataframe)
    pandas_data_viewer.showPandas()

    # Shows the "DataViewerWindow" object
    data_viewer_window.showMaximized()

    # Ends the application when everything is closed
    sys.exit(app.exec_())
