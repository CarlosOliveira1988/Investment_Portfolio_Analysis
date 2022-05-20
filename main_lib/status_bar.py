"""This file is responsible to define the 'Status Bar' of the application."""


from gui_lib.pushbutton import StandardPushButton
from PyQt5 import QtCore, QtWidgets


class StatusBar:
    """Class used to create the 'Status Bar' of the main application."""

    def __init__(self):
        """Create the StatusBar object."""
        # Update Button
        self.update_btn = QtWidgets.QPushButton("Reabrir Planilha Extrato")
        self.update_btn.setFixedSize(
            QtCore.QSize(
                StandardPushButton.DEFAULT_WIDTH,
                StandardPushButton.DEFAULT_HEIGHT,
            )
        )

        # Status Bar
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.addPermanentWidget(self.update_btn)

    """Public methods."""

    def getWidget(self):
        """Return the menu widget."""
        return self.status_bar

    def setUpdateButtonEvent(self, function):
        """Set the method related to the onClick button event."""
        self.update_btn.clicked.connect(function)

    def setBarMessage(self, string):
        """Set a message in the status bar."""
        self.status_bar.showMessage(string)
