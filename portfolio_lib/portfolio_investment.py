"""This file has a set of methods related to Portfolio/Extrato."""

import os
import sys

try:
    from portfolio_lib.extrato_manager import ExtratoFileManager
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
    from portfolio_lib.extrato_manager import ExtratoFileManager
    from portfolio_lib.fixed_income import FixedIncomeAssets
    from portfolio_lib.gdrive_exporter import GoogleDriveExporter
    from portfolio_lib.multi_processing import MultiProcessingTasks
    from portfolio_lib.portfolio_history import OperationsHistory
    from portfolio_lib.treasuries import TreasuriesAssets
    from portfolio_lib.variable_income import VariableIncomeAssets


class PortfolioInvestment(ExtratoFileManager):
    """This is a class to manage all portfolio operations."""

    TOTAL_PROCESSES = 2
    EXTRATO_PROCESS_ID = 0
    REALTIME_PROCESS_ID = 1

    def __init__(self, fileOperations=None):
        """Create the PortfolioInvestment object."""
        super().__init__(fileOperations)
        self.VariableIncome = VariableIncomeAssets()
        self.FixedIncome = FixedIncomeAssets()
        self.Treasuries = TreasuriesAssets()
        self.multi_process_list = self.__getProcessList()
        self.run()

    """Private methods."""

    def __getProcessList(self):
        processes = PortfolioInvestment.TOTAL_PROCESSES
        return [MultiProcessingTasks() for x in range(processes)]

    """Protected methods."""

    def _startNewProcess(self, function, proc_index):
        self.multi_process_list[proc_index].startNewProcess(function)

    def _endAllProcesses(self, proc_index):
        self.multi_process_list[proc_index].endAllProcesses()

    def _updateOpenedOperations(self):
        history = OperationsHistory(self.operations.copy())
        self.openedOperations = history.getOpenedOperationsDataframe()
        self.VariableIncome.setOpenedOperations(self.openedOperations)
        self.FixedIncome.setOpenedOperations(self.openedOperations)
        self.Treasuries.setOpenedOperations(self.openedOperations)

    def _updateCurrentPortfolio(self):
        self.currentVariableIncome = self.VariableIncome.currentPortfolio()

    def _updateCurrentRendaFixa(self):
        self.currentFixedIncome = self.FixedIncome.currentRendaFixa()

    def _updateCurrentTesouroDireto(self):
        self.currentTreasuries = self.Treasuries.currentTesouroDireto()

    """Public methods."""

    def run(self):
        """Run the main routines related to the excel porfolio file."""
        # The bellow tasks run in parallel
        proc_id = PortfolioInvestment.EXTRATO_PROCESS_ID
        self._startNewProcess(self._updateOpenedOperations(), proc_id)
        self._endAllProcesses(proc_id)

        # The below tasks run in parallel and are dependent of the above tasks
        proc_id = PortfolioInvestment.REALTIME_PROCESS_ID
        self._startNewProcess(self._updateCurrentPortfolio(), proc_id)
        self._startNewProcess(self._updateCurrentRendaFixa(), proc_id)
        self._startNewProcess(self._updateCurrentTesouroDireto(), proc_id)
        self._endAllProcesses(proc_id)

    def currentPortfolioGoogleDrive(self, auto_save=True, auto_open=True):
        """Save the excel file to be used in Google Drive."""
        return self.VariableIncome.currentPortfolioGoogleDrive(
            self.getExtratoPath(),
            auto_save,
            auto_open,
        )

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
        print("\nCarteira Renda Variável - Google Drive:", carteiraGD)
        print("\nCarteira Renda Variável:", carteiraRV)
        print("\nCarteira Renda Fixa:", carteiraRF)
        print("\nCarteira Tesouro Direto:", tesouro)
    else:
        print("\nThe selected Portfolio file is not in the expected format.")
        print("\nPlease, check the following expected column names:")
        for title in portfolio.getExpectedColumnsTitleList():
            print(" - ", title)
