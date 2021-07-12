from os import replace
from indexer_manager import IndexerManager


class IPCA(IndexerManager):
    def __init__(self):
        super().__init__('IPCA mensal.xlsx')


class SELIC(IndexerManager):
    def __init__(self):
        super().__init__('SELIC mensal.xlsx')


class CDI(IndexerManager):
    def __init__(self):
        super().__init__('CDI mensal.xlsx')


class FGTS(IndexerManager):
    def __init__(self):
        super().__init__('FGTS mensal.xlsx')


class NovaPoupanca(IndexerManager):
    def __init__(self):
        super().__init__('Poupança nova mensal.xlsx')


class AntigaPoupanca(IndexerManager):
    def __init__(self):
        super().__init__('Poupança antiga mensal.xlsx')


class EconomicIndexer:
    """
    This class provides a collection of Economic Indexers.
    """
    def __init__(self):
        self.IPCA = IPCA()
        self.SELIC = SELIC()
        self.CDI = CDI()
        self.FGTS = FGTS()
        self.NovaPoupanca = NovaPoupanca()
        self.AntigaPoupanca = AntigaPoupanca()


# Example of how to use the "EconomicIndexer" class
if __name__ == "__main__":

    # Standard modules imports
    import sys
    from PyQt5 import QtWidgets

    # Add mainfolder path to sys.path
    main_path = sys.path[0]
    main_path = main_path.replace('indexer_lib', '')
    sys.path.append(main_path)

    # Customized modules imports
    from window import Window
    from indexer_formater import OriginalIndexerFormater
    from treeview_pandas import TreeviewPandas

    # Creates the application
    app = QtWidgets.QApplication(sys.argv)

    # Creates the data viewer window
    window = Window('Testing Economic Indexers')

    # Creates the IPCA formated dataframe
    economic_indexer = EconomicIndexer()
    indexer_formater = OriginalIndexerFormater(economic_indexer.IPCA.getDataframe(stacked=False))
    formated_dataframe = indexer_formater.getFormatedDataFrame()

    # Creates the pandas data viewer
    pandas_data_viewer = TreeviewPandas(window.getCentralWidget(), formated_dataframe)
    pandas_data_viewer.showPandas(resize_per_contents=False)

    # Shows the "Window" object
    window.showMaximized()

    # Ends the application when everything is closed
    sys.exit(app.exec_())
