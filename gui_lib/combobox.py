from datetime import datetime

from PyQt5 import QtCore, QtWidgets

from gui_lib.label import StandardLabel
from gui_lib.widget_interface import WidgetInterface


class StandardComboBox(QtWidgets.QComboBox):

    """
    This class is used to create a Standard ComboBox inheriting the "QtWidgets.QComboBox" class.

    Arguments:
    - CentralWidget: the widget where the ComboBox will be placed
    - coordinate_X: the window X coordinate where the ComboBox will be placed
    - coordinate_Y: the window Y coordinate where the ComboBox will be placed
    - width: the width of the ComboBox
    - height: the height of the ComboBox
    - onSelectionMethod: the callback method of the "currentIndexChanged" ComboBox event
    """

    # Contants related to the ComboBox
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(
        self,
        CentralWidget,
        coordinate_X=0,
        coordinate_Y=0,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        onSelectionMethod=None,
    ):
        super().__init__(CentralWidget)
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        if onSelectionMethod:
            self.currentIndexChanged.connect(onSelectionMethod)


class DateComboBox(WidgetInterface):

    """
    This class is used to create a special ComboBox for Date Selection.

    Basically, it is a join of:
    - 1 'QLabel' located in the first line
    - 2 'QComboBox' located in the second and third lines

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
        width=StandardComboBox.DEFAULT_WIDTH,
    ):
        # Internal central widget
        super().__init__(CentralWidget)

        # Date's Label
        self.Label = StandardLabel(
            self, title, coordinate_Y=self.getInternalHeight(), width=width
        )
        self.incrementInternalHeight(self.Label.height())

        # Month's ComboBox
        self.ComboBoxMonth = StandardComboBox(
            self, coordinate_Y=self.getInternalHeight(), width=width
        )
        self.incrementInternalHeight(self.ComboBoxMonth.height())

        # Year's ComboBox
        self.ComboBoxYear = StandardComboBox(
            self, coordinate_Y=self.getInternalHeight(), width=width
        )
        self.incrementInternalHeight(self.ComboBoxYear.height())

        # Widget dimensions
        self.setGeometry(
            QtCore.QRect(coordinate_X, coordinate_Y, width, self.getInternalHeight())
        )

    def addMonthsItems(self, months_list):
        """
        Adds the months strings to be displayed in the comboboxes.
        """
        self.ComboBoxMonth.addItems(months_list)

    def addYearsItems(self, years_list):
        """
        Adds the years strings to be displayed in the comboboxes.
        """
        self.ComboBoxYear.addItems(years_list)

    def getSelectedPeriod(self, as_string=True):
        """
        Returns the selected period (Year and Month).

        If 'as_string' is 'True', return 'Janeiro', 'Fevereiro', etc.
        If 'as_string' is 'False', return '1', '2', etc.
        """
        if as_string:
            return self.ComboBoxYear.currentText(), self.ComboBoxMonth.currentText()
        else:
            return (
                int(self.ComboBoxYear.currentText()),
                self.ComboBoxMonth.currentIndex() + 1,
            )

    def getSelectedPeriodAsDate(self, day=1):
        """
        Returns the selected period as a datetime.
        """
        year, month = self.getSelectedPeriod(as_string=False)
        date_tuple = str(year), str(month), str(day)
        date_string = "/".join(date_tuple)
        return datetime.strptime(date_string, "%Y/%m/%d")
