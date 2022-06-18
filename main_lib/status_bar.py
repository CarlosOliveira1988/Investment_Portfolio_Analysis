"""This file is responsible to define the 'Status Bar' of the application."""


from gui_lib.pushbutton import StandardPushButton
from PyQt5 import QtCore, QtWidgets


class StatusBar:
    """Class used to create the 'Status Bar' of the main application."""

    def __init__(self):
        """Create the StatusBar object."""
        # Buttons
        self.update_btn = self.__addButton("Recarregar XLS")
        self.editxls_btn = self.__addButton("Editar XLS")

        # Status Bar
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.addPermanentWidget(self.update_btn)
        self.status_bar.addPermanentWidget(self.editxls_btn)

    """Private methods."""

    def __addButton(self, title):
        button = QtWidgets.QPushButton(title)
        button.setFixedSize(
            QtCore.QSize(
                StandardPushButton.DEFAULT_WIDTH / 2,
                StandardPushButton.DEFAULT_HEIGHT,
            )
        )
        return button

    """Public methods."""

    def getWidget(self):
        """Return the menu widget."""
        return self.status_bar

    def setUpdateButtonEvent(self, function):
        """Set the method related to the onClick button event."""
        self.update_btn.clicked.connect(function)

    def setEditXlsButtonEvent(self, function):
        """Set the method related to the onClick button event."""
        self.editxls_btn.clicked.connect(function)

    def setBarMessage(self, string):
        """Set a message in the status bar."""
        self.status_bar.showMessage(string)
