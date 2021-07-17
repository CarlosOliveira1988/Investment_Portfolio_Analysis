# Standard modules imports
import sys
from PyQt5 import QtWidgets

# Add mainfolder path to sys.path, in order to allow importing the below customized mudules
main_path = sys.path[0]
main_path = main_path.replace('\\indexer_lib', '')
sys.path.append(main_path)

# Customized modules imports
from window import Window
from treeview_pandas import TreeviewPandas
from economic_indexers_widget import EconomicIndexerWidget

# Creates the application
app = QtWidgets.QApplication(sys.argv)

# Creates the data viewer window
window = Window('Testing Economic Indexers')

# Creates the IPCA formated dataframe
economic_indexer_widget = EconomicIndexerWidget(window.getCentralWidget())

# Shows the "Window" object
window.showMaximized()

# Ends the application when everything is closed
sys.exit(app.exec_())
