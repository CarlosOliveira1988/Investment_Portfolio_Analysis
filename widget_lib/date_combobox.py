from datetime import datetime

from gui_lib.combobox import StandardComboBox
from gui_lib.label import StandardLabel
from PyQt5 import QtCore

from widget_lib.widget_interface import WidgetInterface


class DateComboBox(WidgetInterface):
    """Class used to create a special ComboBox Widget for Date Selection."""

    def __init__(
        self,
        CentralWidget,
        title,
        coordinate_X=0,
        coordinate_Y=0,
        width=StandardComboBox.DEFAULT_WIDTH,
    ):
        """Create a DateComboBox object from "StandardComboBox".

        Basically, it is a join of:
        - 1 'QLabel' located in the first line
        - 2 'QComboBox' located in the second and third lines

        Arguments:
        - CentralWidget: the widget where all the components will be placed
        - title: the text on the label
        - coordinate_X: the window X coordinate inside the widget
        - coordinate_Y: the window Y coordinate inside the widget
        - width: the width value used to create all related components
        """
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
            QtCore.QRect(
                coordinate_X,
                coordinate_Y,
                width,
                self.getInternalHeight(),
            )
        )

    def addMonthsItems(self, months_list):
        """Add the months strings to be displayed in the comboboxes."""
        self.ComboBoxMonth.addItems(months_list)

    def addYearsItems(self, years_list):
        """Add the years strings to be displayed in the comboboxes."""
        self.ComboBoxYear.addItems(years_list)

    def getSelectedPeriod(self, as_string=True):
        """
        Return the selected period (Year and Month).

        If 'as_string' is 'True', return 'Janeiro', 'Fevereiro', etc.
        If 'as_string' is 'False', return '1', '2', etc.
        """
        if as_string:
            result = (
                self.ComboBoxYear.currentText(),
                self.ComboBoxMonth.currentText(),
            )
        else:
            result = (
                int(self.ComboBoxYear.currentText()),
                self.ComboBoxMonth.currentIndex() + 1,
            )
        return result

    def getSelectedPeriodAsDate(self, day=1):
        """Return the selected period as a datetime."""
        year, month = self.getSelectedPeriod(as_string=False)
        date_tuple = str(year), str(month), str(day)
        date_string = "/".join(date_tuple)
        return datetime.strptime(date_string, "%Y/%m/%d")
