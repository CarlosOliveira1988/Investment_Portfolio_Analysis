from PyQt5 import QtWidgets
from PyQt5 import QtCore

from gui_lib.label import StandardLabel


class StandardLineEdit:
    """ 
    This class is used to create a Standard Line Edit.

    Arguments:
    - CentralWidget: the widget where the line edit will be placed
    - coordinate_X: the window X coordinate where the line edit will be placed
    - coordinate_Y: the window Y coordinate where the line edit will be placed
    - width: the width of the line edit
    - height: the height of the line edit
    """

    # Contants related to the push button
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(self, CentralWidget, coordinate_X=0, coordinate_Y=0, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        # Dimensions
        self.width = width
        self.height = height

        # Initialization
        self.LineEdit = QtWidgets.QLineEdit(CentralWidget)
        self.LineEdit.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height


class ParameterLineEdit:
    """ 
    This class is used to create a special Line Edit for user value input.

    Basically, it is a join of:
    - a 'QLabel' located in the first line
    - a 'QLineEdit' located in the second line

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    - title: the text on the label
    - coordinate_X: the window X coordinate where the label will be placed
    - coordinate_Y: the window Y coordinate where the label will be placed
    - width: the width value used to create both 'QLabel' and 'QLineEdit' components
    """

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, width=StandardLineEdit.DEFAULT_WIDTH):
        # Width
        self.width = width
        self.height = StandardLabel.DEFAULT_HEIGHT + StandardLineEdit.DEFAULT_HEIGHT
        
        # Label
        Label_coordinate_X = coordinate_X
        Label_coordinate_Y = coordinate_Y
        self.StandardLabel = StandardLabel(CentralWidget, title, Label_coordinate_X, Label_coordinate_Y, width=width)

        # LineEdit
        LineEdit_coordinate_X = coordinate_X
        LineEdit_coordinate_Y = Label_coordinate_Y + StandardLabel.DEFAULT_HEIGHT
        self.StandardLineEdit = StandardLineEdit(CentralWidget, LineEdit_coordinate_X, LineEdit_coordinate_Y, width=width)

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
