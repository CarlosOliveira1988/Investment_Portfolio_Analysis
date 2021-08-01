# Define the constants
FILE_NAME = '\PORTFOLIO_TEMPLATE.xlsx'
FILE_SHEET = r'Extrato'

# Creates the application
import sys
from PyQt5 import QtWidgets
from window import Window
from treeview_pandas import TreeviewPandas
from extrato import readOperations
app = QtWidgets.QApplication(sys.argv)

# Get the path of the main folder 'Investment_Portfolio_Analysis'
def getMainPath():
    return sys.path[0]

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
