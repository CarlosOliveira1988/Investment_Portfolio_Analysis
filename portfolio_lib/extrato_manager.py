"""This file is useful to handle extrato spreadsheet file."""

import os

import pandas as pd


class ExtratoFileManager:
    """This is a class to manage the extrato file."""

    def __init__(self, fileOperations=None):
        """Create the ExtratoFileManager object."""
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
        self.setFile(fileOperations)

    """Private methods."""

    def __getFileOperationsPath(self):
        try:
            if os.path.isfile(self.fileOperations):
                return os.path.dirname(self.fileOperations)
            elif os.path.isdir(self.fileOperations):
                return self.fileOperations
        except TypeError:
            return None

    def __updateOperations(self):
        self.operations = self.__readExtrato()

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

    def __getDefaultExtrato(self):
        col_list = self.getExpectedColumnsTitleList()
        return pd.DataFrame(columns=col_list)

    def __readExtrato(self):
        try:
            extrato = pd.read_excel(self.fileOperations)
            extrato = extrato[self.expected_title_list]
            # Excel file has title and data lines
            if self.__isValidFile(extrato):
                self.valid_file = True
                return extrato
            # Excel file has ONLY the title line
            else:
                self.valid_file = False
                return self.__getDefaultExtrato()
        except ValueError:
            self.valid_file = False
            return self.__getDefaultExtrato()
        except FileNotFoundError:
            self.valid_file = False
            return self.__getDefaultExtrato()
        except KeyError:
            self.valid_file = False
            return self.__getDefaultExtrato()

    """Public methods."""

    def getExpectedColumnsTitleList(self):
        """Return a list of expected column titles."""
        return self.expected_title_list.copy()

    def getExtratoPath(self):
        """Get the extrato sheet path.

        Return 'None' if 'fileOperations' is not a file.
        """
        return self.__getFileOperationsPath()

    def getExtrato(self):
        """Return the raw dataframe related to the excel porfolio file."""
        return self.operations.copy()

    def isValidFile(self):
        """Return if the excel portfolio file is valid or not."""
        return self.valid_file

    def setFile(self, fileOperations):
        """Set the excel file related to the porfolio."""
        self.fileOperations = fileOperations
        self.fileOperationsPath = self.__getFileOperationsPath()
        self.__updateOperations()
