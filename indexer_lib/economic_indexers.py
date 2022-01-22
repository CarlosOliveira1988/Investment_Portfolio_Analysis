from indexer_lib.indexer_manager import IndexerManager


class IPCA(IndexerManager):
    def __init__(self):
        super().__init__("IPCA.xlsx")


class SELIC(IndexerManager):
    def __init__(self):
        super().__init__("SELIC.xlsx")


class CDI(IndexerManager):
    def __init__(self):
        super().__init__("CDI.xlsx")


class FGTS(IndexerManager):
    def __init__(self):
        super().__init__("FGTS.xlsx")


class NovaPoupanca(IndexerManager):
    def __init__(self):
        super().__init__("Poupanca.xlsx")


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

    def getNamesList(self):
        return self.__dict__.keys()
