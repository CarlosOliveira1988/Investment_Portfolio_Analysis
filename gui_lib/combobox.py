from PyQt5 import QtWidgets
from PyQt5 import QtCore

from gui_lib.label import StandardLabel


class StandardComboBox:
    """ 
    This class is used to create a Standard Combo Box.

    Arguments:
    - CentralWidget: the widget where the combo box will be placed
    - coordinate_X: the window X coordinate where the combo box will be placed
    - coordinate_Y: the window Y coordinate where the combo box will be placed
    - width: the width of the combo box
    - height: the height of the combo box
    - onSelectionMethod: the callback method of the "currentIndexChanged" event
    """

    # Contants related to the combo box
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(self, CentralWidget, coordinate_X=0, coordinate_Y=0, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, onSelectionMethod=None):
        # Dimensions
        self.width = width
        self.height = height

        # Initialization
        self.ComboBox = QtWidgets.QComboBox(CentralWidget)
        self.ComboBox.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        if onSelectionMethod:
            self.ComboBox.currentIndexChanged.connect(onSelectionMethod)

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height


class DateComboBox:
    """ 
    This class is used to create a special Combo Box for Date Selection.

    Basically, it is a join of:
    - 1 'QLabel' located in the first line
    - 2 'QComboBox' located in the second and third lines

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    - title: the text on the label
    - coordinate_X: the window X coordinate where the label will be placed
    - coordinate_Y: the window Y coordinate where the label will be placed
    - width: the width value used to create both 'QLabel' and 'QLineEdit' components
    """

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, width=StandardComboBox.DEFAULT_WIDTH):
        # Dimensions
        self.width = width
        self.height = StandardLabel.DEFAULT_HEIGHT + 2*StandardComboBox.DEFAULT_HEIGHT

        # Date's Label
        self.Label = StandardLabel(CentralWidget, title, coordinate_X=coordinate_X, coordinate_Y=coordinate_Y, width=width)

        # Month's ComboBox
        CbMonth_coordinate_X = coordinate_X
        CbMonth_coordinate_Y = coordinate_Y + StandardLabel.DEFAULT_HEIGHT
        self.CbMonth = StandardComboBox(CentralWidget, coordinate_X=CbMonth_coordinate_X,
        coordinate_Y=CbMonth_coordinate_Y, width=width)
        
        # Year's ComboBox
        CbYear_coordinate_X = coordinate_X
        CbYear_coordinate_Y = CbMonth_coordinate_Y + StandardComboBox.DEFAULT_HEIGHT
        self.CbYear = StandardComboBox(CentralWidget, coordinate_X=CbYear_coordinate_X,
        coordinate_Y=CbYear_coordinate_Y, width=width)

    def addMonthsItems(self, months_list):
        self.CbMonth.ComboBox.addItems(months_list)

    def addYearsItems(self, years_list):
        self.CbYear.ComboBox.addItems(years_list)

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
