"""File used to get the main configuration parameters for the project."""

import os

from dotenv import load_dotenv


class ExtratoFileManager:
    """Class used to handle .ENV files to get main configurations."""

    def __init__(self):
        """Create the ExtratoFileManager object."""
        self.__loadDotEnvFile()
        if not self.__dotEnvFileExists():
            self.__saveDotEnvFile(self.__getDefaultExtratoFile())
        self.extrato_file = self.__getExtratoFile()

    """Private methods."""

    def __loadDotEnvFile(self):
        load_dotenv(encoding="iso-8859-1")

    def __saveDotEnvFile(self, filename):
        with open(".env", "w") as file:
            file.write("EXTRATO_PATH=" + filename)

    def __dotEnvFileExists(self):
        # When the .ENV file does not exist; or
        # When the parameter does not exist inside the .ENV file;
        # Then the 'dotenv' API returns 'None'
        return self.__getUserExtratoFile() is not None

    def __getDefaultExtratoFile(self):
        """Return the default Extrato spreadsheet file path.

        This file can be found inside the projetct folders.
        """
        DEFAULT_DIRECTORY = os.path.join(os.getcwd(), "portfolio_lib")
        FILE_NAME = "PORTFOLIO_TEMPLATE_EMPTY.xlsx"
        return os.path.join(DEFAULT_DIRECTORY, FILE_NAME)

    def __getUserExtratoFile(self):
        """Return the Extrato spreadsheet file path defined in .env file."""
        return os.getenv("EXTRATO_PATH")

    def __isValidExtratoFile(self, file):
        try:
            return os.path.isfile(file)
        except TypeError:
            return False

    def __getExtratoFile(self):
        user_file = self.__getUserExtratoFile()
        if self.__isValidExtratoFile(user_file):
            return user_file
        else:
            return self.__getDefaultExtratoFile()

    """Public methods."""

    def getExtratoFile(self):
        """Return the Extrato spreadsheet file.

        When the user file is not found, then returns the default file.
        """
        return self.extrato_file

    def setExtratoFile(self, file):
        """Set the path related to the Extrato spreadsheet in the .ENV file."""
        self.__saveDotEnvFile(file)
        self.extrato_file = file
