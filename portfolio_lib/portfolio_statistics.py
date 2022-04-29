"""This file is useful to show some valid statistics related to Portfolio."""


class PortfolioStatistcs:
    """This is a class to manage statistics related to portfolio."""

    def __init__(self):
        """Create the PortfolioStatistcs object."""
        self.operations = None

    """Public methods."""

    def setOperations(self, operations):
        """Set the opened operations."""
        self.operations = operations.copy()

    def overallTaxAndIncomes(self):
        """Return the sum of the fees, income tax, dividend and jcp."""
        fee = self.operations["Taxas"].sum()
        incomeTax = self.operations["IR"].sum()
        dividend = self.operations["Dividendos"].sum()
        jcp = self.operations["JCP"].sum()
        return fee, incomeTax, dividend, jcp

    def numberOperationsYear(self):
        """Return 3 lists containing the number of operations.

        The lists are linked between themselves according to the year.
        """
        dataframe = self.operations.copy()
        firstYear = dataframe["Data"].min()
        lastYear = dataframe["Data"].max()

        # Creates the empty lists
        listYear = []
        listBuy = []
        listSell = []
        janFirst = "-01-01"  # Auxiliary variable for the first day of the year
        decLast = "-12-31"  # Auxiliary variable for he last day of the year

        # Collects the number of operations per year
        if len(dataframe):
            for i in range(firstYear.year, lastYear.year + 1):
                start = str(i) + janFirst
                end = str(i) + decLast
                # Get filtered table according to the year
                filtered = dataframe[
                    (dataframe["Data"] >= start) & (dataframe["Data"] <= end)
                ]
                filteredBuy = filtered[(filtered["Operação"] == "Compra")]
                filteredSell = filtered[(filtered["Operação"] == "Venda")]
                # Add the values in the lists
                listYear.append(i)
                listBuy.append(len(filteredBuy.index))
                listSell.append(len(filteredSell.index))

        return listYear, listBuy, listSell

    def operationsByTicker(self, ticker):
        """Return a filtered dataframe according to the ticker.

        The input for the method is the file that holds the operations.
        The filter is done based on this file.
        """
        dataframe = self.operations[self.operations["Ticker"] == ticker]
        return dataframe

    def unitsTicker(self, ticker):
        """Return how many stocks of the given ticker."""
        # Filter the table by ticker
        dataframe = self.operationsByTicker(ticker)

        # Filter the table by buy operation
        buy = dataframe[dataframe["Operação"] == "Compra"]

        # Calculate the number of units bought
        buy = int(buy["Quantidade"].sum())

        # Filter the table by sell operation
        sell = dataframe[dataframe["Operação"] == "Venda"]

        # Calculate the number of units sold
        sell = int(sell["Quantidade"].sum())

        return buy, sell, buy - sell

    def earningsByTicker(self, ticker):
        """Return the total earnings of a given ticker."""
        dataframe = self.operationsByTicker(ticker)
        dataframe = dataframe[dataframe["Operação"] == "Provento"]
        return float(dataframe["Dividendos"].sum() + dataframe["JCP"].sum())

    def avgPriceTicker(self, ticker):
        """Return the average price of a given ticker."""
        dataframe = self.operationsByTicker(ticker)

        # Fill with 0 the data that is not fullfilled in the dataframe.
        # It is important because non filled cells will return NaN,
        # which will cause calculation issues.
        dataframe = dataframe.fillna(0)

        avgPrice = 0
        avgPriceOld = 0
        qtStock = 0.0
        qtStockOld = 0.0
        costs = 0
        for index, row in dataframe.iterrows():
            # If the current operation is a buy event,
            # then update the average price
            if row["Operação"] == "Compra":
                # Get some useful data
                qtStock = row["Quantidade"]
                unitPrice = row["Preço Unitário"]
                costs = row["Taxas"] + row["IR"]

                # Calculate the average price of the operation
                avgPrice = (qtStock * unitPrice + costs) / qtStock

                # Calculate the average price considering also
                # the previous operations
                oldStockPrice = avgPriceOld * qtStockOld
                curStockPrice = avgPrice * qtStock
                qtStockTotal = qtStockOld + qtStock
                avgPrice = (oldStockPrice + curStockPrice) / qtStockTotal
                avgPriceOld = avgPrice
                qtStockOld += qtStock

            # If the current operation is a sell event,
            # then updates the number of stocks
            elif row["Operação"] == "Venda":
                qtStock -= row["Quantidade"]
                qtStockOld -= row["Quantidade"]

        # numberStocks = qtStockOld
        return avgPrice, qtStockOld

    def customTable(
        self,
        ticker,
        market,
        dueDate,
        profitability,
        index,
        operation,
    ):
        """Read the Excel file with all the operations.

        Return a filtered dataframe according with the desired parameters.
        """
        df = self.operations
        if ticker != "all":
            df = df[df["Ticker"] == ticker]
        if market != "all":
            df = df[df["Mercado"] == market]
        if dueDate != "NA":
            df = df[df["Vencimento"] == dueDate]
        if profitability != "NA":
            df = df[df["Rentabilidade Contratada"] == dueDate]
        if index != "all":
            df = df[df["Indexador"] == index]
        if operation != "all":
            df = df[df["Operação"] == operation]
        return df

    def customTableDate(
        self,
        ticker,
        market,
        dueDate,
        profitability,
        index,
        operation,
        startDate,
        endDate,
    ):
        """Read the Excel file with all the operations.

        Return a filtered dataframe according with the desired parameters
        and a certain time range.
        """
        dataframe = self.customTable(
            ticker, market, dueDate, profitability, index, operation
        )
        dataframe = dataframe[dataframe["Data"] >= startDate]
        dataframe = dataframe[dataframe["Data"] <= endDate]
        return dataframe
