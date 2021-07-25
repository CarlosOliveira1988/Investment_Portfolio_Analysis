from PyQt5 import QtWidgets
from PyQt5 import QtCore


class StandardLabel(QtWidgets.QLabel):
    
    """ 
    This class is used to create a Standard Label inheriting the "QtWidgets.QLabel" class.

    Arguments:
    - CentralWidget: the widget where the Label will be placed
    - title: the text on the Label
    - coordinate_X: the window X coordinate where the Label will be placed
    - coordinate_Y: the window Y coordinate where the Label will be placed
    - width: the width of the Label
    - height: the height of the Label
    """

    # Contants related to the push button
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        super().__init__(CentralWidget)
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        self.setText(title)
