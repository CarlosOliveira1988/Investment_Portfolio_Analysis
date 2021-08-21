"""This file has a set of classes related to "QtWidgets.QPushButton"."""

from PyQt5 import QtCore, QtWidgets


class StandardPushButton(QtWidgets.QPushButton):
    """Class to create a StandardPushButton with "QtWidgets.QPushButton"."""

    # Contants related to the PushButton
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
        onClickMethod=None,
    ):
        """
        Create an StandardPushButton object from "QtWidgets.QPushButton".

        Arguments:
        - CentralWidget: the widget where the PushButton will be placed
        - title: the text on the PushButton
        - coordinate_X: the window X coordinate inside the widget
        - coordinate_Y: the window Y coordinate inside the widget
        - width: the width of the PushButton
        - height: the height of the PushButton
        - onClickMethod: the callback method of the "onClick" PushButton event
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
        if onClickMethod:
            self.clicked.connect(onClickMethod)
