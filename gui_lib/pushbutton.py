from PyQt5 import QtWidgets
from PyQt5 import QtCore


class StandardPushButton:
    """ 
    This class is used to create a Standard Push Button.

    Arguments:
    - CentralWidget: the widget where the push button will be placed
    - title: the text on the button
    - coordinate_X: the window X coordinate where the PushButton will be placed
    - coordinate_Y: the window Y coordinate where the PushButton will be placed
    - width: the width of the PushButton
    - height: the height of the PushButton
    - onClickMethod: the callback method of the "onClick" event
    """

    # Contants related to the push button
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, onClickMethod=None):
        # Dimensions
        self.width = width
        self.height = height

        # Initialization
        self.PushButton = QtWidgets.QPushButton(CentralWidget)
        self.PushButton.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        self.PushButton.setText(title)
        if onClickMethod:
            self.PushButton.clicked.connect(onClickMethod)

    """
    Public methods
    """
    def setTitle(self, title):
        """
        Set the text shown in the button.
        """
        self.PushButton.setText(title)

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
