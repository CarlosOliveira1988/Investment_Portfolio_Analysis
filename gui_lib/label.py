"""This file has a set of classes related to "QtWidgets.QLabel"."""

from PyQt5 import QtCore, QtWidgets


class StandardLabel(QtWidgets.QLabel):
    """Class used to create a StandardLabel with "QtWidgets.QLabel"."""

    # Contants related to the push button
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(
        self,
        CentralWidget,
        title,
        coordinate_X=0,
        coordinate_Y=0,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
    ):
        """Create a StandardLabel object rom "QtWidgets.QLabel".

        Arguments:
        - CentralWidget: the widget where the Label will be placed
        - title: the text on the Label
        - coordinate_X: the window X coordinate inside the widget
        - coordinate_Y: the window Y coordinate inside the widget
        - width: the width of the Label
        - height: the height of the Label
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
        self.setText(title)
