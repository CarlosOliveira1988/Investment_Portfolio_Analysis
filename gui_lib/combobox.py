"""This file has a set of classes related to "QtWidgets.QComboBox"."""

from PyQt5 import QtCore, QtWidgets


class StandardComboBox(QtWidgets.QComboBox):
    """Class used to create a StandardComboBox with "QtWidgets.QComboBox"."""

    # Contants related to the ComboBox
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(
        self,
        CentralWidget,
        coordinate_X=0,
        coordinate_Y=0,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        onSelectionMethod=None,
    ):
        """Create a StandardComboBox object from "QtWidgets.QComboBox".

        Arguments:
        - CentralWidget: the widget where the ComboBox will be placed
        - coordinate_X: the window X coordinate inside the widget
        - coordinate_Y: the window Y coordinate inside the widget
        - width: the width of the ComboBox
        - height: the height of the ComboBox
        - onSelectionMethod: the callback method of the "currentIndexChanged"
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
        if onSelectionMethod:
            self.currentIndexChanged.connect(onSelectionMethod)
