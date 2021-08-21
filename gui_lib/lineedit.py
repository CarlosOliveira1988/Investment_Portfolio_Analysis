"""This file has a set of classes related to "QtWidgets.QLineEdit"."""

from PyQt5 import QtCore, QtWidgets


class StandardLineEdit(QtWidgets.QLineEdit):
    """Class to create a StandardLineEdit with "QtWidgets.QLineEdit"."""

    # Contants related to the LineEdit
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(
        self,
        CentralWidget,
        coordinate_X=0,
        coordinate_Y=0,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
    ):
        """
        Create an StandardLineEdit object from "QtWidgets.QLineEdit".

        Arguments:
        - CentralWidget: the widget where the LineEdit will be placed
        - coordinate_X: the window X coordinate inside the widget
        - coordinate_Y: the window Y coordinate inside the widget
        - width: the width of the LineEdit
        - height: the height of the LineEdit
        """
        super().__init__(CentralWidget)
        self.setGeometry(
            QtCore.QRect(
                coordinate_X,
                coordinate_Y,
                width,
                height,
            )
        )
