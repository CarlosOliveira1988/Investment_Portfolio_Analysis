from PyQt5 import QtWidgets
from PyQt5 import QtCore


class StandardLabel:
    """ 
    This class is used to create a Standard Label.

    Arguments:
    - CentralWidget: the widget where the label will be placed
    - title: the text on the label
    - coordinate_X: the window X coordinate where the label will be placed
    - coordinate_Y: the window Y coordinate where the label will be placed
    - width: the width of the label
    - height: the height of the label
    """

    # Contants related to the push button
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        # Dimensions
        self.width = width
        self.height = height

        # Initialization
        self.Label = QtWidgets.QLabel(CentralWidget)
        self.Label.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        self.Label.setText(title)

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
