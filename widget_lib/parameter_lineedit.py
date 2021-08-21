"""This file has a special widget based on "QtWidgets.QLineEdit"."""

from gui_lib.label import StandardLabel
from gui_lib.lineedit import StandardLineEdit
from PyQt5 import QtCore

from widget_lib.widget_interface import WidgetInterface


class ParameterLineEdit(WidgetInterface):
    """Class to create a ParameterLineEdit with "StandardLineEdit"."""

    def __init__(
        self,
        CentralWidget,
        title,
        coordinate_X=0,
        coordinate_Y=0,
        width=StandardLineEdit.DEFAULT_WIDTH,
    ):
        """Create a ParameterLineEdit object from "StandardLineEdit".

        Basically, it is used for any type of input user value using:
        - a 'QLabel' located in the first line
        - a 'QLineEdit' located in the second line

        Arguments:
        - CentralWidget: the widget where all the components will be placed
        - title: the text on the label
        - coordinate_X: the window X coordinate inside the widget
        - coordinate_Y: the window Y coordinate inside the widget
        - width: the width value used to create all related components
        """
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
            QtCore.QRect(
                coordinate_X,
                coordinate_Y,
                width,
                self.getInternalHeight(),
            )
        )
