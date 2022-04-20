"""This file has a set of methods related to Portfolio/Extrato."""

import os
import sys

import pandas as pd
import yfinance as yf

try:
    from portfolio_lib.fixed_income import FixedIncomeAssets
    from portfolio_lib.gdrive_exporter import GoogleDriveExporter
    from portfolio_lib.multi_processing import MultiProcessingTasks
    from portfolio_lib.portfolio_history import OperationsHistory
    from portfolio_lib.treasuries import TreasuriesAssets
    from portfolio_lib.variable_income import VariableIncomeAssets

except ModuleNotFoundError:

    # Change the directory
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    # Run the import statements
    from portfolio_lib.fixed_income import FixedIncomeAssets
    from portfolio_lib.gdrive_exporter import GoogleDriveExporter
    from portfolio_lib.multi_processing import MultiProcessingTasks
    from portfolio_lib.portfolio_history import OperationsHistory
    from portfolio_lib.treasuries import TreasuriesAssets
    from portfolio_lib.variable_income import VariableIncomeAssets


class PortfolioInvestment:
    """This is a class to manage all portfolio operations."""

    TOTAL_PROCESSES = 2
    EXTRATO_PROCESS_ID = 0
    REALTIME_PROCESS_ID = 1

    def __init__(self, fileOperations=None):
        """Create the PortfolioInvestment object."""
        self.VariableIncome = VariableIncomeAssets()
        self.FixedIncome = FixedIncomeAssets()
        self.Treasuries = TreasuriesAssets()
        self.expected_title_list = [
            "Mercado",
            "Ticker",
            "Operação",
            "Data",
            "Rentabilidade Contratada",
            "Indexador",
            "Vencimento",
            "Quantidade",
            "Preço Unitário",
            "Preço Total",
            "Taxas",
            "IR",
            "Dividendos",
            "JCP",
            "Custo Total",
            "Notas",
        ]
        self.multi_process_list = self.__getProcessList()
        self.setFile(fileOperations)
        self.run()

    def __getProcessList(self):
        processes = PortfolioInvestment.TOTAL_PROCESSES
        return [MultiProcessingTasks() for x in range(processes)]

    def getExpectedColumnsTitleList(self):
        """Return a list of expected column titles."""
        return self.expected_title_list

    def setFile(self, fileOperations):
        """Set the excel file related to the porfolio."""
        self.fileOperations = fileOperations
        self._updateOperations()

    def getExtratoPath(self):
        """Get the extrato sheet path."""
        if os.path.isfile(self.fileOperations):
            return os.path.dirname(self.fileOperations)
        elif os.path.isdir(self.fileOperations):
            return self.fileOperations

    def isValidFile(self):
        """Return if the excel portfolio file is valid or not."""
        return self.valid_file

    def __isValidFile(self, extrato):
        """Return if the excel portfolio file is valid or not."""
        valid_flag = True
        # If some expected column is not present in the excel file
        # or the title line is empty in the excel file,
        # then the file is not valid
        if list(extrato):
            for expected_title in self.expected_title_list:
                if expected_title not in extrato:
                    valid_flag = False
                    break
        else:
            valid_flag = False
        return valid_flag

    def _startNewProcess(self, function, proc_index):
        self.multi_process_list[proc_index].startNewProcess(function)

    def _endAllProcesses(self, proc_index):
        self.multi_process_list[proc_index].endAllProcesses()

    def run(self):
        """Run the main routines related to the excel porfolio file."""
        # The bellow tasks run in parallel
        proc_id = PortfolioInvestment.EXTRATO_PROCESS_ID
        self._startNewProcess(self._updateOpenedOperations(), proc_id)
        self._startNewProcess(self._updateOperationsYear(), proc_id)
        self._endAllProcesses(proc_id)

        # The below tasks run in parallel and are dependent of the above tasks
        proc_id = PortfolioInvestment.REALTIME_PROCESS_ID
        self._startNewProcess(self._updateCurrentPortfolio(), proc_id)
        self._startNewProcess(self._updateCurrentRendaFixa(), proc_id)
        self._startNewProcess(self._updateCurrentTesouroDireto(), proc_id)
        self._endAllProcesses(proc_id)

    def _updateOperations(self):
        self.operations = self._readExtrato()

    def _updateOpenedOperations(self):
        history = OperationsHistory(self.operations.copy())
        self.openedOperations = history.getOpenedOperationsDataframe()
        self.VariableIncome.setOpenedOperations(self.openedOperations)
        self.FixedIncome.setOpenedOperations(self.openedOperations)
        self.Treasuries.setOpenedOperations(self.openedOperations)

    def _updateOperationsYear(self):
        self.operationsYear = self.numberOperationsYear()

    def _updateCurrentPortfolio(self):
        self.currentVariableIncome = self.VariableIncome.currentPortfolio()

    def _updateCurrentRendaFixa(self):
        self.currentFixedIncome = self.FixedIncome.currentRendaFixa()

    def _updateCurrentTesouroDireto(self):
        self.currentTreasuries = self.Treasuries.currentTesouroDireto()

    def _getDefaultExtrato(self):
        col_list = self.getExpectedColumnsTitleList()
        return pd.DataFrame(columns=col_list)

    def _readExtrato(self):
        try:
            extrato = pd.read_excel(self.fileOperations)
            # Excel file has title and data lines
            if self.__isValidFile(extrato):
                self.valid_file = True
                return extrato
            # Excel file has ONLY the title line
            else:
                self.valid_file = False
                return self._getDefaultExtrato()
        except ValueError:
            self.valid_file = False
            return self._getDefaultExtrato()

    def getExtrato(self):
        """Return the raw dataframe related to the excel porfolio file."""
        return self.operations.copy()

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

    def tesouroSelic(self):
        """Return all operations related to Tesouro SELIC."""
        dataframe = self.operations[
            self.operations["Mercado"] == "Tesouro Direto",
        ]
        dataframe = dataframe[
            dataframe["Indexador"] == "SELIC",
        ]
        return dataframe

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

    def currentMarketPriceByTicker(self, ticker):
        """Return the last price of the stock."""
        # I had issues when downloading data for Fundos imobiliários.
        # It was necessary to work with period of 30d.
        # I believe that is mandatory period or start/end date.
        # With start/end I also had issues for reading the values.
        # The solution was to consider "30d" as the period.
        # I compared the results from function in Google and they were correct.
        dataframe = yf.download(ticker, period="30d")
        data = dataframe["Adj Close"].tail(1)
        return float(data)

    def sectorOfTicker(self, ticker):
        """Return the sector of a given ticker.

        The function uses the yfinance library to get the information.
        """
        ticker = ticker + ".SA"
        data = yf.Ticker(ticker)
        return data.info["sector"]

    def currentPortfolioGoogleDrive(self):
        """Save the excel file to be used in Google Drive."""
        exporter = GoogleDriveExporter()
        exporter.save(self.currentPortfolio(), self.getExtratoPath())

    def currentPortfolio(self):
        """Create a dataframe with all opened operations of Renda Variável."""
        return self.currentVariableIncome.copy()

    def currentTesouroDireto(self):
        """Create a dataframe with all opened operations of Tesouro Direto."""
        return self.currentTreasuries.copy()

    def currentRendaFixa(self):
        """Create a dataframe with all opened operations of Renda Fixa."""
        return self.currentFixedIncome.copy()


if __name__ == "__main__":

    import os

    # Main directory
    SOURCE_FILE_DIRECTORY = os.path.join(os.path.curdir, "portfolio_lib")
    FILE_NAME = "PORTFOLIO_TEMPLATE_PERFORMANCE.xlsx"
    FILE = os.path.join(SOURCE_FILE_DIRECTORY, FILE_NAME)

    # Example:
    portfolio = PortfolioInvestment(FILE)
    if portfolio.isValidFile():
        carteiraGD = portfolio.currentPortfolioGoogleDrive()
        carteiraRV = portfolio.currentPortfolio()
        carteiraRF = portfolio.currentRendaFixa()
        tesouro = portfolio.currentTesouroDireto()
        print("\nCarteira Renda Variável:", carteiraRV)
        print("\nCarteira Renda Fixa:", carteiraRF)
        print("\nCarteira Tesouro Direto:", tesouro)
    else:
        print("\nThe selected Portfolio file is not in the expected format.")
        print("\nPlease, check the following expected column names:")
        for title in portfolio.getExpectedColumnsTitleList():
            print(" - ", title)
