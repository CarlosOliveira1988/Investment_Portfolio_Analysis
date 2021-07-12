from window import Window
from treeview import Treeview


class TreeviewPandas(Treeview):
    """ 
    This class provides methods and attributes to show Pandas DataFrames in a table.

    Arguments:
    - CentralWidget: the widget where the table will be placed
    - PandasDataFrame: the pandas dataframe
    """
    def __init__(self, CentralWidget, PandasDataFrame):
        self.PandasDataFrame = PandasDataFrame
        super().__init__(CentralWidget, list(self.PandasDataFrame))

    def showPandas(self, resize_per_contents=True):
        for line_data_row in self.PandasDataFrame.itertuples(index=False):
            line_data_row_list = list(line_data_row)
            items_list = self.convertValuesListToItemsList(line_data_row_list)
            self.insertParentLine(items_list)
            if resize_per_contents:
                self.resizeColumnsToContents()


# Example of how to use the "TreeviewPandas" class
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

    # Creates the data viewer window
    window = Window('Testing Pandas Data Viewer')

    # Creates the pandas dataframe
    source_file_directory = getMainPath()
    pandas_dataframe = readOperations(source_file_directory + FILE_NAME)

    # Creates the pandas data viewer
    pandas_data_viewer = TreeviewPandas(window.getCentralWidget(), pandas_dataframe)
    pandas_data_viewer.showPandas()

    # Shows the "Window" object
    window.showMaximized()

    # Ends the application when everything is closed
    sys.exit(app.exec_())
