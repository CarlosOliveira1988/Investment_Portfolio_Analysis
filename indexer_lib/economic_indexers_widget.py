from PyQt5 import QtGui
from PyQt5 import QtCore

from economic_indexers import EconomicIndexer
from treeview_pandas import TreeviewPandas
from window import Window
from gui_lib.tab import StandardTab
from gui_lib.combobox import DateComboBox
from gui_lib.combobox import StandardComboBox
from gui_lib.lineedit import ParameterLineEdit
from gui_lib.pushbutton import StandardPushButton
from gui_lib.widget_interface import WidgetInterface


class InterestRateSelection(WidgetInterface):

    """ 
    This class is used to create a special widget for interest rate selection.

    Basically, it is a join of:
    - a 'QLabel' located in the first line
    - a 'QLineEdit' located in the second line
    - a 'QComboBox' located in the third line

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    - title: the text on the label
    - coordinate_X: the window X coordinate where the components will be placed
    - coordinate_Y: the window Y coordinate where the components will be placed
    - width: the width value used to create all related components
    """

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, width=StandardComboBox.DEFAULT_WIDTH):
        # Internal central widget
        super().__init__(CentralWidget)

        # ParameterLineEdit
        self.ParameterLineEdit = ParameterLineEdit(self, title, coordinate_Y=self.getInternalHeight(), width=width)
        self.ParameterLineEdit.LineEdit.setValidator(QtGui.QDoubleValidator())
        self.incrementInternalHeight(self.ParameterLineEdit.height())

        # ComboBox
        self.StandardComboBox = StandardComboBox(self, coordinate_Y=self.getInternalHeight(), width=width)
        self.StandardComboBox.addItems(['Nenhum', 'Prefixado (+)', 'Proporcional (x)'])
        self.incrementInternalHeight(self.StandardComboBox.height())

        # Widget dimensions
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, self.getInternalHeight()))

    def setDefaultValues(self, default_type_number=0):
        if default_type_number == 0:
            self.ParameterLineEdit.LineEdit.setText('0,00')
            self.StandardComboBox.setCurrentIndex(0)
        elif default_type_number == 1:
            self.ParameterLineEdit.LineEdit.setText('0,00')
            self.StandardComboBox.setCurrentIndex(1)
        elif default_type_number == 2:
            self.ParameterLineEdit.LineEdit.setText('100,00')
            self.StandardComboBox.setCurrentIndex(2)


class ParameterWidget(WidgetInterface):

    """ 
    This class is used to create a special widget for user input. Here we have the following parameters:
    - Initial Value
    - Initial Period
    - Final Period
    - Additional Interest Rate

    Additionaly, we have some buttons to perform calculation and graph plotting.

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    - coordinate_X: the window X coordinate where the components will be placed
    - coordinate_Y: the window Y coordinate where the components will be placed
    """

    # Contants related to the widget
    WIDTH = StandardComboBox.DEFAULT_WIDTH / 2
    EMPTY_SPACE = StandardComboBox.DEFAULT_HEIGHT

    def __init__(self, CentralWidget, coordinate_X=0, coordinate_Y=0):
        # Internal central widget
        super().__init__(CentralWidget)

        # Initial Value
        self.InitialValue = ParameterLineEdit(self, 'Valor Inicial (R$)', coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.InitialValue.LineEdit.setValidator(QtGui.QDoubleValidator())
        self.incrementInternalHeight(self.InitialValue.height() + ParameterWidget.EMPTY_SPACE)

        # Initial Period selection
        self.InitialPeriod = DateComboBox(self, 'Período Inicial', coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.incrementInternalHeight(self.InitialPeriod.height() + ParameterWidget.EMPTY_SPACE)
        
        # Final Period selection
        self.FinalPeriod = DateComboBox(self, 'Período Final', coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.incrementInternalHeight(self.FinalPeriod.height() + ParameterWidget.EMPTY_SPACE)

        # Additional Interest Rate
        self.InterestRate = InterestRateSelection(self, 'Taxa Adicional (%)', coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.incrementInternalHeight(self.InterestRate.height() + ParameterWidget.EMPTY_SPACE)

        # Calculate button
        self.Calculate = StandardPushButton(self, 'Calcular', coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.incrementInternalHeight(self.Calculate.height() + ParameterWidget.EMPTY_SPACE)

        # Plot button
        self.Plot = StandardPushButton(self, 'Gráfico', coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.incrementInternalHeight(self.Plot.height() + ParameterWidget.EMPTY_SPACE)

        # Default button
        self.Default = StandardPushButton(self, 'Restaurar', coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.incrementInternalHeight(self.Default.height())

        # Widget dimensions
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, ParameterWidget.WIDTH, self.getInternalHeight()))

    def setDefaultValues(self, default_type_number=0):
        self.InitialValue.LineEdit.setText('1000,00')

        self.InitialPeriod.ComboBoxMonth.setCurrentIndex(0)
        self.InitialPeriod.ComboBoxYear.setCurrentIndex(0)

        self.FinalPeriod.ComboBoxMonth.setCurrentIndex(0)
        self.FinalPeriod.ComboBoxYear.setCurrentIndex(0)

        self.InterestRate.setDefaultValues(default_type_number)

    def setMonthsItems(self, months_list):
        self.InitialPeriod.ComboBoxMonth.addItems(months_list)
        self.FinalPeriod.ComboBoxMonth.addItems(months_list)
    
    def setYearsItems(self, years_list):
        self.InitialPeriod.ComboBoxYear.addItems(years_list)
        self.FinalPeriod.ComboBoxYear.addItems(years_list)


class IndexerPanelWidget(WidgetInterface):

    """ 
    This class is used to create a special widget for user input related to some Economic Indexer.

    Basically, we have:
    - a widget to enter some data and perform some calculation/plotting graphs
    - a treeview table

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    - dataframe: a pandas dataframe with formated data to be displayed in the treeview table
    - coordinate_X: the window X coordinate where the components will be placed
    - coordinate_Y: the window Y coordinate where the components will be placed
    - width: the width of the widget
    """

    # Contants related to the widget
    EMPTY_SPACE = StandardComboBox.DEFAULT_HEIGHT

    def __init__(self, CentralWidget, dataframe, coordinate_X, coordinate_Y, width):
        # Internal central widget
        super().__init__(CentralWidget)

        # ParameterWidget
        self.ParameterWidget = ParameterWidget(self, coordinate_X=self.getInternalWidth(), coordinate_Y=0)
        self.incrementInternalWidth(self.ParameterWidget.width() + IndexerPanelWidget.EMPTY_SPACE)

        # TreeviewPandas
        self.TreeviewPandas = TreeviewPandas(self, dataframe, coordinate_X=self.getInternalWidth(), coordinate_Y=0, width=width-self.getInternalWidth(), height=self.ParameterWidget.height())
        self.TreeviewPandas.showPandas()
        self.TreeviewPandas.resizeColumnsToTreeViewWidth()
        self.incrementInternalWidth(self.TreeviewPandas.width())

        # Widget dimensions
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, self.getInternalWidth(), self.ParameterWidget.height()))

    def setMonthsItems(self, months_list):
        months_list = [str(month) for month in months_list]
        self.ParameterWidget.InitialPeriod.ComboBoxMonth.addItems(months_list)
        self.ParameterWidget.FinalPeriod.ComboBoxMonth.addItems(months_list)
    
    def setYearsItems(self, years_list):
        years_list = [str(year) for year in years_list]
        self.ParameterWidget.InitialPeriod.ComboBoxYear.addItems(years_list)
        self.ParameterWidget.FinalPeriod.ComboBoxYear.addItems(years_list)

    def setDefaultValues(self, indexer_name):
        if ('IPCA' in indexer_name) or ('SELIC' in indexer_name):
            self.ParameterWidget.setDefaultValues(1)
        elif ('CDI' in indexer_name):
            self.ParameterWidget.setDefaultValues(2)
        else:
            self.ParameterWidget.setDefaultValues(0)


class EconomicIndexerWidget:

    TAB_WIDTH = 1300
    TAB_HEIGHT = 660

    TAB_WIDTH_USEFUL = TAB_WIDTH - 2*Window.DEFAULT_BORDER_SIZE
    TAB_HEIGHT_USEFUL = TAB_HEIGHT - 3*Window.DEFAULT_BORDER_SIZE

    def __init__(self, CentralWidget):
        # Economic indexers (IPCA, SELIC, etc.)
        self.Indexers = EconomicIndexer()

        # Tab panel widget
        self.TabPanel = StandardTab(CentralWidget, width=EconomicIndexerWidget.TAB_WIDTH, height=EconomicIndexerWidget.TAB_HEIGHT)

        # Fill the tabs according to each Economic Indexer available
        for indexer_name in self.Indexers.getNamesList():
            tab_central_widget = self.TabPanel.addNewTab(indexer_name)
            dataframe = self.Indexers.__getattribute__(indexer_name).getFormatedDataframe(False)
            coordinate_X = Window.DEFAULT_BORDER_SIZE
            coordinate_Y = Window.DEFAULT_BORDER_SIZE
            width = EconomicIndexerWidget.TAB_WIDTH_USEFUL
            indexer_panel = IndexerPanelWidget(tab_central_widget, dataframe, coordinate_X=coordinate_X, coordinate_Y=coordinate_Y, width=width)
            indexer_panel.setMonthsItems(self.Indexers.__getattribute__(indexer_name).getMonthsList())
            indexer_panel.setYearsItems(self.Indexers.__getattribute__(indexer_name).getYearsList())
            indexer_panel.setDefaultValues(indexer_name)
