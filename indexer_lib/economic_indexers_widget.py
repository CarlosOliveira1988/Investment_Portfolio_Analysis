from PyQt5 import QtGui, QtWidgets

from economic_indexers import EconomicIndexer
from treeview_pandas import TreeviewPandas
from window import Window
from gui_lib.tab import StandardTab
from gui_lib.combobox import DateComboBox
from gui_lib.combobox import StandardComboBox
from gui_lib.lineedit import ParameterLineEdit
from gui_lib.pushbutton import StandardPushButton


class InterestRateSelection:
    """ 
    This class is used to create a special widget for interest rate selection.

    Basically, it is a join of:
    - a 'QLabel' located in the first line
    - a 'QLineEdit' located in the second line
    - a 'QComboBox' located in the third line

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    - title: the text on the label
    - coordinate_X: the window X coordinate where the label will be placed
    - coordinate_Y: the window Y coordinate where the label will be placed
    - width: the width value used to create all components
    """

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, width=StandardComboBox.DEFAULT_WIDTH):
        # Width
        self.width = width

        # Label and LineEdit
        self.ParameterLineEdit = ParameterLineEdit(CentralWidget, title, coordinate_X, coordinate_Y, width=width)
        self.ParameterLineEdit.StandardLineEdit.LineEdit.setValidator(QtGui.QDoubleValidator())

        # ComboBox
        combobox_coordinate_X = coordinate_X
        combobox_coordinate_Y = coordinate_Y + self.ParameterLineEdit.getHeight()
        self.StandardComboBox = StandardComboBox(CentralWidget, combobox_coordinate_X, combobox_coordinate_Y, width=width)
        self.StandardComboBox.ComboBox.addItems(['Nenhum', 'Prefixado (+)', 'Proporcional (x)'])

    def setDefaultValues(self, default_type_number=0):
        if default_type_number == 0:
            self.ParameterLineEdit.StandardLineEdit.LineEdit.setText('0,00')
            self.StandardComboBox.ComboBox.setCurrentIndex(0)
        elif default_type_number == 1:
            self.ParameterLineEdit.StandardLineEdit.LineEdit.setText('0,00')
            self.StandardComboBox.ComboBox.setCurrentIndex(1)
        elif default_type_number == 2:
            self.ParameterLineEdit.StandardLineEdit.LineEdit.setText('100,00')
            self.StandardComboBox.ComboBox.setCurrentIndex(2)

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.ParameterLineEdit.getHeight() + StandardComboBox.DEFAULT_HEIGHT


class ParameterWidget:

    WIDTH = StandardComboBox.DEFAULT_WIDTH / 2
    EMPTY_SPACE = StandardComboBox.DEFAULT_HEIGHT

    def __init__(self, CentralWidget, coordinate_X, coordinate_Y):
        # Widget dimensions
        self.width = ParameterWidget.WIDTH
        self.height = 0

        # Widget internal coordinates
        self.coordinate_X = coordinate_X
        self.coordinate_Y = coordinate_Y

        # Initial Value
        self.InitialValue = ParameterLineEdit(CentralWidget, 'Valor Inicial (R$)', self.coordinate_X, self.coordinate_Y, width=self.width)
        self.__incrementWidgetHeight(self.InitialValue)
        self.__incrementWidgetCoordinateY(self.InitialValue, add_empty_space=True)
        self.InitialValue.StandardLineEdit.LineEdit.setValidator(QtGui.QDoubleValidator())

        # Initial Period selection
        self.InitialPeriod = DateComboBox(CentralWidget, 'Período Inicial', self.coordinate_X, self.coordinate_Y, width=self.width)
        self.__incrementWidgetHeight(self.InitialPeriod)
        self.__incrementWidgetCoordinateY(self.InitialPeriod, add_empty_space=True)
        
        # Final Period selection
        self.FinalPeriod = DateComboBox(CentralWidget, 'Período Final', self.coordinate_X, self.coordinate_Y, width=self.width)
        self.__incrementWidgetHeight(self.FinalPeriod)
        self.__incrementWidgetCoordinateY(self.FinalPeriod, add_empty_space=True)

        # Additional Interest Rate
        self.InterestRate = InterestRateSelection(CentralWidget, 'Taxa Adicional (%)', self.coordinate_X, self.coordinate_Y, width=self.width)
        self.__incrementWidgetHeight(self.InterestRate)
        self.__incrementWidgetCoordinateY(self.InterestRate, add_empty_space=True)

        # Calculate button
        self.Calculate = StandardPushButton(CentralWidget, 'Calcular', self.coordinate_X, self.coordinate_Y, width=self.width)
        self.__incrementWidgetHeight(self.Calculate)
        self.__incrementWidgetCoordinateY(self.Calculate, add_empty_space=True)

        # Plot button
        self.Plot = StandardPushButton(CentralWidget, 'Gráfico', self.coordinate_X, self.coordinate_Y, width=self.width)
        self.__incrementWidgetHeight(self.Plot)
        self.__incrementWidgetCoordinateY(self.Plot, add_empty_space=True)

        # Default button
        self.Default = StandardPushButton(CentralWidget, 'Restaurar', self.coordinate_X, self.coordinate_Y, width=self.width)
        self.__incrementWidgetHeight(self.Default)
        self.__incrementWidgetCoordinateY(self.Default, add_empty_space=False)

    """
    Private methods
    """
    def __incrementWidgetHeight(self, widget):
        self.height += widget.getHeight()

    def __incrementWidgetCoordinateY(self, widget, add_empty_space=True):
        if add_empty_space:
            self.coordinate_Y += (widget.getHeight() + ParameterWidget.EMPTY_SPACE)
        else:
            self.coordinate_Y += (widget.getHeight() + 0)

    """
    Public methods
    """
    def setDefaultValues(self, default_type_number=0):
        self.InitialValue.StandardLineEdit.LineEdit.setText('1000,00')

        self.InitialPeriod.CbMonth.ComboBox.setCurrentIndex(0)
        self.InitialPeriod.CbYear.ComboBox.setCurrentIndex(0)

        self.FinalPeriod.CbMonth.ComboBox.setCurrentIndex(0)
        self.FinalPeriod.CbYear.ComboBox.setCurrentIndex(0)

        self.InterestRate.setDefaultValues(default_type_number)

    def setMonthsItems(self, months_list):
        self.InitialPeriod.CbMonth.ComboBox.addItems(months_list)
        self.FinalPeriod.CbMonth.ComboBox.addItems(months_list)
    
    def setYearsItems(self, years_list):
        self.InitialPeriod.CbYear.ComboBox.addItems(years_list)
        self.FinalPeriod.CbYear.ComboBox.addItems(years_list)

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height


class EconomicIndexerWidget:

    TAB_WIDTH = 1300
    TAB_HEIGTH = 660

    TAB_WIDTH_USEFUL = TAB_WIDTH - 2*Window.DEFAULT_BORDER_SIZE
    TAB_HEIGTH_USEFUL = TAB_HEIGTH - 3*Window.DEFAULT_BORDER_SIZE

    def __init__(self, CentralWidget):
        self.Indexers = EconomicIndexer()
        self.__Tab = StandardTab(CentralWidget, width=EconomicIndexerWidget.TAB_WIDTH, height=EconomicIndexerWidget.TAB_HEIGTH)
        self.__addTabs()

    def __addTreeview(self, tab_central_widget, name, treeview_coordinate_X):
        dataframe = self.Indexers.__getattribute__(name).getFormatedDataframe(False)
        coordinate_X = treeview_coordinate_X
        coordinate_Y = Window.DEFAULT_BORDER_SIZE
        width = EconomicIndexerWidget.TAB_WIDTH_USEFUL - treeview_coordinate_X + Window.DEFAULT_BORDER_SIZE
        height = EconomicIndexerWidget.TAB_HEIGTH_USEFUL
        new_treeview = TreeviewPandas(
            tab_central_widget, dataframe,
            coordinate_X=coordinate_X, coordinate_Y=coordinate_Y,
            width=width, height=height
        )
        new_treeview.showPandas()
        new_treeview.resizeColumnsToTreeViewWidth()

    def __addParameterWidget(self, tab_central_widget, name):
        coordinate_X = Window.DEFAULT_BORDER_SIZE
        coordinate_Y = Window.DEFAULT_BORDER_SIZE
        new_parameter_widget = ParameterWidget(tab_central_widget, coordinate_X, coordinate_Y)
        self.__setParameterInitialValues(name, new_parameter_widget)
        final_coordinate_X = new_parameter_widget.getWidth() + 2*Window.DEFAULT_BORDER_SIZE
        return final_coordinate_X

    def __setParameterInitialValues(self, name, new_parameter_widget):
        months_list = self.Indexers.__getattribute__(name).getMonthsList()
        new_parameter_widget.setMonthsItems(months_list)
        years_list = self.Indexers.__getattribute__(name).getYearsList()
        years_list = [str(year) for year in years_list]
        new_parameter_widget.setYearsItems(years_list)
        if ('IPCA' in name) or ('SELIC' in name):
            new_parameter_widget.setDefaultValues(1)
        elif ('CDI' in name):
            new_parameter_widget.setDefaultValues(2)
        else:
            new_parameter_widget.setDefaultValues(0)

    def __addTabs(self):
        for name in self.Indexers.getNamesList():
            tab_central_widget = self.__Tab.addTab(name)
            treeview_coordinate_X = self.__addParameterWidget(tab_central_widget, name)
            self.__addTreeview(tab_central_widget, name, treeview_coordinate_X)
