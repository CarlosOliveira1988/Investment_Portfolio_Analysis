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
