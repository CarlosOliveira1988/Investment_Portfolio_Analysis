"""This file is used to test the 'months_indexers.py'."""

from indexer_lib.months_indexers import TwelveMonthsIndexer


class Test_TwelveMonthsIndexer:
    """Tests for 'TwelveMonthsIndexer' class."""

    def testGetValues(self):
        """Test the get methods."""
        indexers = TwelveMonthsIndexer()
        # Usually, CDI and IPCA are greater than 1%/year
        assert indexers.getIPCA() >= 0.01
        assert indexers.getCDI() >= 0.01
        assert indexers.getSELIC() >= 0.01
