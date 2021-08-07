from PyQt5 import QtWidgets
from PyQt5 import QtCore


class StandardTextEdit(QtWidgets.QTextEdit):

    """ 
    This class is used to create a Standard TextEdit inheriting the "QtWidgets.QTextEdit" class.

    Arguments:
    - CentralWidget: the widget where the TextEdit will be placed
    - coordinate_X: the window X coordinate where the TextEdit will be placed
    - coordinate_Y: the window Y coordinate where the TextEdit will be placed
    - width: the width of the TextEdit
    - height: the height of the TextEdit
    """

    # Contants related to the TextEdit
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 500

    def __init__(self, CentralWidget, coordinate_X=0, coordinate_Y=0, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        super().__init__(CentralWidget)
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
