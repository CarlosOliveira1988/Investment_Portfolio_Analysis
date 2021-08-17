import sys

from PyQt5 import QtCore, QtWidgets

# Add mainfolder path to sys.path, in order to allow importing the customized mudules
main_path = sys.path[0]
main_path = main_path.replace("\\indexer_lib", "")
sys.path.append(main_path)

# Customized modules imports
from window import Window

from economic_indexers_widget import EconomicIndexerWidget


class EconomicIndexerWindow(Window):
    def __init__(self, auto_show=True):
        super().__init__("Indicadores Econômicos")

        # Indexer Widget
        self.IndexerWidget = EconomicIndexerWidget(self.getCentralWidget())

        # Window dimensions
        self.setGeometry(
            QtCore.QRect(
                0,
                0,
                self.IndexerWidget.getInternalWidth(),
                self.IndexerWidget.getInternalHeight(),
            )
        )
        self.setFixedSize(
            self.IndexerWidget.getInternalWidth(),
            self.IndexerWidget.getInternalHeight(),
        )

        # Show the window
        if auto_show:
            self.show()


if __name__ == "__main__":

    # Create the application
    app = QtWidgets.QApplication(sys.argv)

    # Creates the data viewer window
    window = EconomicIndexerWindow()

    # Ends the application when everything is closed
    sys.exit(app.exec_())
