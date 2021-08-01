from PyQt5 import QtWidgets
from PyQt5 import QtCore


class StandardPushButton(QtWidgets.QPushButton):
    
    """ 
    This class is used to create a Standard PushButton inheriting the "QtWidgets.QPushButton" class.

    Arguments:
    - CentralWidget: the widget where the PushButton will be placed
    - title: the text on the PushButton
    - coordinate_X: the window X coordinate where the PushButton will be placed
    - coordinate_Y: the window Y coordinate where the PushButton will be placed
    - width: the width of the PushButton
    - height: the height of the PushButton
    - onClickMethod: the callback method of the "onClick" PushButton event
    """

    # Contants related to the PushButton
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, onClickMethod=None):
        super().__init__(CentralWidget)
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        self.setText(title)
        if onClickMethod:
            self.clicked.connect(onClickMethod)
