"""This file has a set of classes related to "QtWidgets.QTextEdit"."""

from PyQt5 import QtCore, QtWidgets


class StandardTextEdit(QtWidgets.QTextEdit):
    """Class used to create a StandardTextEdit with "QtWidgets.QTextEdit"."""

    # Contants related to the TextEdit
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 500

    def __init__(
        self,
        CentralWidget,
        coordinate_X=0,
        coordinate_Y=0,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
    ):
        """
        Create an StandardTextEdit object from "QtWidgets.QTextEdit".

        Arguments:
        - CentralWidget: the widget where the TextEdit will be placed
        - coordinate_X: the window X coordinate inside the widget
        - coordinate_Y: the window Y coordinate inside the widget
        - width: the width of the TextEdit
        - height: the height of the TextEdit
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
