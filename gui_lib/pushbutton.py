"""This file has a set of classes related to "QtWidgets.QPushButton"."""

from PyQt5 import QtCore, QtWidgets


class StandardPushButton(QtWidgets.QPushButton):
    """Class to create a StandardPushButton with "QtWidgets.QPushButton"."""

    # Contants related to the PushButton
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(
        self,
        CentralWidget=None,
        title="",
        coordinate_X=0,
        coordinate_Y=0,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        onClickMethod=None,
        autosize=False,
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

        # If specified by 'autosize' flag, then the main class controls the
        # parent widget by 'addWidget()' method using GridLayouts
        if autosize:
            super().__init__()
        else:
            super().__init__(CentralWidget)

        # Set fixed size if not using the 'autosize' feature
        if autosize:
            pass
        else:
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
