"""This file has a kind of interface based on "QtWidgets.QWidget"."""

from PyQt5 import QtWidgets


class WidgetInterface(QtWidgets.QWidget):
    """Class used to create a WidgetInterface with "QtWidgets.QWidget"."""

    def __init__(self, CentralWidget):
        """Create an WidgetInterface object from "QtWidgets.QWidget".

        Arguments:
        - CentralWidget: the parent widget where this widget is placed
        """
        super().__init__(CentralWidget)
        self.__width = 0
        self.__height = 0

    def incrementInternalWidth(self, width):
        """Increment the internal widget width."""
        self.__width += width

    def getInternalWidth(self):
        """Return the internal widget width."""
        return self.__width

    def incrementInternalHeight(self, height):
        """Increment the internal widget height."""
        self.__height += height

    def getInternalHeight(self):
        """Return the internal widget height."""
        return self.__height
