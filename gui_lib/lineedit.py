from PyQt5 import QtCore, QtWidgets

from gui_lib.label import StandardLabel
from gui_lib.widget_interface import WidgetInterface


class StandardLineEdit(QtWidgets.QLineEdit):

    """
    This class is used to create a Standard LineEdit inheriting the "QtWidgets.QLineEdit" class.

    Arguments:
    - CentralWidget: the widget where the LineEdit will be placed
    - coordinate_X: the window X coordinate where the LineEdit will be placed
    - coordinate_Y: the window Y coordinate where the LineEdit will be placed
    - width: the width of the LineEdit
    - height: the height of the LineEdit
    """

    # Contants related to the LineEdit
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(
        self,
        CentralWidget,
        coordinate_X=0,
        coordinate_Y=0,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
    ):
        super().__init__(CentralWidget)
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))


class ParameterLineEdit(WidgetInterface):

    """
    This class is used to create a special LineEdit for any type of user value input.

    Basically, it is a join of:
    - a 'QLabel' located in the first line
    - a 'QLineEdit' located in the second line

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    - title: the text on the label
    - coordinate_X: the window X coordinate where the components will be placed
    - coordinate_Y: the window Y coordinate where the components will be placed
    - width: the width value used to create all related components
    """

    def __init__(
        self,
        CentralWidget,
        title,
        coordinate_X=0,
        coordinate_Y=0,
        width=StandardLineEdit.DEFAULT_WIDTH,
    ):
        # Internal central widget
        super().__init__(CentralWidget)

        # Label
        self.Label = StandardLabel(
            self, title, coordinate_Y=self.getInternalHeight(), width=width
        )
        self.incrementInternalHeight(self.Label.height())

        # LineEdit
        self.LineEdit = StandardLineEdit(
            self, coordinate_Y=self.getInternalHeight(), width=width
        )
        self.incrementInternalHeight(self.LineEdit.height())

        # Widget dimensions
        self.setGeometry(
            QtCore.QRect(coordinate_X, coordinate_Y, width, self.getInternalHeight())
        )
