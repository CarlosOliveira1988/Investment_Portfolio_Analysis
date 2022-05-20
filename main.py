"""This is the main file of the project."""

import atexit
import sys

from PyQt5 import QtWidgets

from main_lib.main_config import ExtratoFileManager
from main_lib.main_window import MainWindow


def saveEnvConfig():
    """Save the ENV configuration."""
    extrato_manager.setExtratoFile(main.getExtratoFile())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    extrato_manager = ExtratoFileManager()
    main = MainWindow(extrato_manager.getExtratoFile())
    atexit.register(saveEnvConfig)
    sys.exit(app.exec_())
