from datetime import datetime
from PyQt5 import QtGui
from PyQt5 import QtCore

from economic_indexers import EconomicIndexer
from treeview_pandas import TreeviewPandas
from window import Window
from dataframe_filter import DataframeFilter
from interest_calculation import InterestCalculation
from gui_lib.tab import StandardTab
from gui_lib.combobox import DateComboBox
from gui_lib.combobox import StandardComboBox
from gui_lib.lineedit import ParameterLineEdit
from gui_lib.pushbutton import StandardPushButton
from gui_lib.widget_interface import WidgetInterface
from treeview_format import TreeviewValueFormat


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

    ADDITIONAL_RATE_NONE = 'Nenhum    '
    ADDITIONAL_RATE_NONE_INDEX = 0
    ADDITIONAL_RATE_NONE_DEFAULT = '0,00'

    ADDITIONAL_RATE_PREFIXED = 'Prefixado (+)'
    ADDITIONAL_RATE_PREFIXED_INDEX = 1
    ADDITIONAL_RATE_PREFIXED_DEFAULT = '0,00'

    ADDITIONAL_RATE_PROPORTIONAL = 'Proporcional (x)'
    ADDITIONAL_RATE_PROPORTIONAL_INDEX = 2
    ADDITIONAL_RATE_PROPORTIONAL_DEFAULT = '100,00'

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, width=StandardComboBox.DEFAULT_WIDTH):
        # Internal central widget
        super().__init__(CentralWidget)

        # ParameterLineEdit
        self.ParameterLineEdit = ParameterLineEdit(self, title, coordinate_Y=self.getInternalHeight(), width=width)
        self.ParameterLineEdit.LineEdit.setValidator(QtGui.QDoubleValidator())
        self.incrementInternalHeight(self.ParameterLineEdit.height())

        # ComboBox
        self.StandardComboBox = StandardComboBox(self, coordinate_Y=self.getInternalHeight(), width=width)
        self.StandardComboBox.addItem(InterestRateSelection.ADDITIONAL_RATE_NONE)
        self.StandardComboBox.addItem(InterestRateSelection.ADDITIONAL_RATE_PREFIXED)
        self.StandardComboBox.addItem(InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL)
        self.incrementInternalHeight(self.StandardComboBox.height())

        # Widget dimensions
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, self.getInternalHeight()))

    """
    Puclic methods
    """
    def isAdditionalRateNone(self):
        return self.StandardComboBox.currentIndex() == InterestRateSelection.ADDITIONAL_RATE_NONE_INDEX

    def isAdditionalRatePrefixed(self):
        return self.StandardComboBox.currentIndex() == InterestRateSelection.ADDITIONAL_RATE_PREFIXED_INDEX

    def isAdditionalRateProportional(self):
        return self.StandardComboBox.currentIndex() == InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL_INDEX

    def setDefaultValues(self, default_type_number=ADDITIONAL_RATE_NONE_INDEX):
        if default_type_number == InterestRateSelection.ADDITIONAL_RATE_NONE_INDEX:
            self.ParameterLineEdit.LineEdit.setText(InterestRateSelection.ADDITIONAL_RATE_NONE_DEFAULT)
            self.StandardComboBox.setCurrentIndex(InterestRateSelection.ADDITIONAL_RATE_NONE_INDEX)
        elif default_type_number == InterestRateSelection.ADDITIONAL_RATE_PREFIXED_INDEX:
            self.ParameterLineEdit.LineEdit.setText(InterestRateSelection.ADDITIONAL_RATE_PREFIXED_DEFAULT)
            self.StandardComboBox.setCurrentIndex(InterestRateSelection.ADDITIONAL_RATE_PREFIXED_INDEX)
        elif default_type_number == InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL_INDEX:
            self.ParameterLineEdit.LineEdit.setText(InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL_DEFAULT)
            self.StandardComboBox.setCurrentIndex(InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL_INDEX)
    
    def getAdditionalInterestRate(self):
        interest_rate_value = self.ParameterLineEdit.LineEdit.text()
        interest_rate_value =  interest_rate_value.replace(',', '.')
        interest_rate_value = float(interest_rate_value)
        return interest_rate_value / 100
    
    def getAdditionalInterestRateTypeString(self):
        selected_text = self.StandardComboBox.currentText()
        return selected_text[:-4]


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
    - onCalculateClick: the callback method of the "onClick" event
    """

    WIDTH = StandardComboBox.DEFAULT_WIDTH / 2
    EMPTY_SPACE = StandardComboBox.DEFAULT_HEIGHT

    INITIAL_VALUE_LABEL = 'Valor Inicial (R$)'
    INITIAL_PERIOD_LABEL = 'Período Inicial'
    FINAL_PERIOD_LABEL = 'Período Final'
    ADDITIONAL_INTEREST_RATE_LABEL = 'Taxa Adicional (%)'
    CALCULATE_BUTTON_LABEL = 'Calcular'
    PLOT_BUTTON_LABEL = 'Gráfico'
    DEFAULT_BUTTON_LABEL = 'Restaurar'

    INITIAL_VALUE_DEFAULT = '1000,00'

    def __init__(self, CentralWidget, coordinate_X=0, coordinate_Y=0, onCalculateClick=None):
        # Internal central widget
        super().__init__(CentralWidget)

        # Initial Value
        self.InitialValue = ParameterLineEdit(self, ParameterWidget.INITIAL_VALUE_LABEL, coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.InitialValue.LineEdit.setValidator(QtGui.QDoubleValidator())
        self.incrementInternalHeight(self.InitialValue.height() + ParameterWidget.EMPTY_SPACE)

        # Initial Period selection
        self.InitialPeriod = DateComboBox(self, ParameterWidget.INITIAL_PERIOD_LABEL, coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.incrementInternalHeight(self.InitialPeriod.height() + ParameterWidget.EMPTY_SPACE)
        
        # Final Period selection
        self.FinalPeriod = DateComboBox(self, ParameterWidget.FINAL_PERIOD_LABEL, coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.incrementInternalHeight(self.FinalPeriod.height() + ParameterWidget.EMPTY_SPACE)

        # Additional Interest Rate
        self.InterestRate = InterestRateSelection(self, ParameterWidget.ADDITIONAL_INTEREST_RATE_LABEL, coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.incrementInternalHeight(self.InterestRate.height() + ParameterWidget.EMPTY_SPACE)

        # Calculate button
        self.Calculate = StandardPushButton(self, ParameterWidget.CALCULATE_BUTTON_LABEL, coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH, onClickMethod=onCalculateClick)
        self.incrementInternalHeight(self.Calculate.height() + ParameterWidget.EMPTY_SPACE)

        # Plot button
        self.Plot = StandardPushButton(self, ParameterWidget.PLOT_BUTTON_LABEL, coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.Plot.setEnabled(False)
        self.incrementInternalHeight(self.Plot.height() + ParameterWidget.EMPTY_SPACE)

        # Default button
        self.Default = StandardPushButton(self, ParameterWidget.DEFAULT_BUTTON_LABEL, coordinate_Y=self.getInternalHeight(), width=ParameterWidget.WIDTH)
        self.Default.setEnabled(False)
        self.incrementInternalHeight(self.Default.height())

        # Widget dimensions
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, ParameterWidget.WIDTH, self.getInternalHeight()))

        # Auxiliary variables
        self.months_list = []
        self.years_list = []

    """
    Puclic methods
    """
    def setDefaultValues(self, default_type_number=0):
        self.InitialValue.LineEdit.setText(ParameterWidget.INITIAL_VALUE_DEFAULT)

        self.InitialPeriod.ComboBoxMonth.setCurrentIndex(0)
        self.InitialPeriod.ComboBoxYear.setCurrentIndex(0)

        self.FinalPeriod.ComboBoxMonth.setCurrentIndex(0)
        self.FinalPeriod.ComboBoxYear.setCurrentIndex(0)

        self.InterestRate.setDefaultValues(default_type_number)

    def setMonthsItems(self, months_list):
        self.months_list = months_list
        self.InitialPeriod.ComboBoxMonth.addItems(months_list)
        self.FinalPeriod.ComboBoxMonth.addItems(months_list)
    
    def setYearsItems(self, years_list):
        self.years_list = years_list
        self.InitialPeriod.ComboBoxYear.addItems(years_list)
        self.FinalPeriod.ComboBoxYear.addItems(years_list)

    def getSelectedPeriod(self):
        inital_period = self.InitialPeriod.getSelectedPeriodAsDate()
        final_period = self.FinalPeriod.getSelectedPeriodAsDate()
        return inital_period, final_period

    def isValidSelectedPeriod(self):
        inital_period, final_period = self.getSelectedPeriod()
        return final_period >= inital_period
    
    def getInitialValue(self):
        initial_value = self.InitialValue.LineEdit.text()
        initial_value = initial_value.replace(',', '.')
        return float(initial_value)

    def getAdditionalInterestRate(self):
        return self.InterestRate.getAdditionalInterestRate()

    def getAdditionalInterestRateTypeString(self):
        return self.InterestRate.getAdditionalInterestRateTypeString()

    def isAdditionalRateNone(self):
        return self.InterestRate.isAdditionalRateNone()

    def isAdditionalRatePrefixed(self):
        return self.InterestRate.isAdditionalRatePrefixed()

    def isAdditionalRateProportional(self):
        return self.InterestRate.isAdditionalRateProportional()


class IndexerPanelWidget(WidgetInterface):

    """ 
    This class is used to create a special widget for user input related to some Economic Indexer.

    Basically, we have:
    - a widget to enter some data and perform some calculation/plotting graphs
    - a treeview table

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    - indexer_name: the name of the Economic Indexer
    - stacked_dataframe: a pandas dataframe with stacked data useful to perform calculation
    - formated_dataframe: a pandas dataframe with formated data to be displayed in the treeview table
    - coordinate_X: the window X coordinate where the components will be placed
    - coordinate_Y: the window Y coordinate where the components will be placed
    - width: the width of the widget
    """

    EMPTY_SPACE = StandardComboBox.DEFAULT_HEIGHT

    def __init__(self, CentralWidget, indexer_name, stacked_dataframe, formated_dataframe, coordinate_X, coordinate_Y, width):
        # Internal central widget
        super().__init__(CentralWidget)

        # ParameterWidget
        self.ParameterWidget = ParameterWidget(self, coordinate_X=self.getInternalWidth(), coordinate_Y=0, onCalculateClick=self.onCalculateClick)
        self.incrementInternalWidth(self.ParameterWidget.width() + IndexerPanelWidget.EMPTY_SPACE)

        # TreeviewPandas
        self.TreeviewPandas = TreeviewPandas(self, formated_dataframe, coordinate_X=self.getInternalWidth(), coordinate_Y=0, width=width-self.getInternalWidth(), height=self.ParameterWidget.height())
        self.TreeviewPandas.showPandas()
        self.TreeviewPandas.resizeColumnsToTreeViewWidth()
        self.incrementInternalWidth(self.TreeviewPandas.width())

        # Auxiliary variables
        self.indexer_name = indexer_name
        self.stacked_dataframe = self.__adjustStackedDataframe(stacked_dataframe)
        self.DataframeFilter = DataframeFilter()
        self.InterestCalculation = InterestCalculation()

        # Widget dimensions
        self.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, self.getInternalWidth(), self.ParameterWidget.height()))

    def __adjustStackedDataframe(self, stacked_dataframe):
        # Years list
        years_as_number_list = stacked_dataframe['Ano'].tolist()
        years_as_number_list = [int(year) for year in years_as_number_list]

        # Months list
        months_list = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        months_as_string_list = stacked_dataframe['Mês'].tolist()
        months_as_number_list = [months_list.index(month)+1 for month in months_as_string_list]

        # Adjusted date list
        adjusted_date_list = [str(years_as_number_list[i])+'/'+str(months_as_number_list[i])+'/1' for i in range(len(months_as_number_list))]
        adjusted_date_list = [datetime.strptime(adjusted_date, '%Y/%m/%d') for adjusted_date in adjusted_date_list]

        # New column
        adjusted_stacked_dataframe = stacked_dataframe
        adjusted_stacked_dataframe.insert(2, 'Data Ajustada', adjusted_date_list, True)
        adjusted_stacked_dataframe = adjusted_stacked_dataframe[['Data Ajustada', 'Taxa Mensal']]
        return adjusted_stacked_dataframe

    """
    Puclic methods
    """
    def calculateValuesPerIndexerCurve(self, initial_value, monthly_interest_rate_list):
        final_value = initial_value + self.InterestCalculation.calculateInterestValue(monthly_interest_rate_list, initial_value)
        cumulative_interest_value_list = self.InterestCalculation.getCumulativeInterestValueList(monthly_interest_rate_list, initial_value)
        cumulative_monthly_interest_rate_list = self.InterestCalculation.getCumulativeInterestRateList(cumulative_interest_value_list, initial_value)
        return final_value, cumulative_interest_value_list, cumulative_monthly_interest_rate_list

    def sumValuesPerPrefixedInterestRate(self, initial_value, monthly_interest_rate_list, cumulative_interest_value_list):
        additional_rate_per_month = self.InterestCalculation.calculateMeanInterestRatePerPeriod(self.ParameterWidget.getAdditionalInterestRate(), 12)
        additional_monthly_interest_rate_list = self.InterestCalculation.getPrefixedInterestRateList(additional_rate_per_month, len(monthly_interest_rate_list))
        additional_cumulative_interest_value_list = self.InterestCalculation.getCumulativeInterestValueList(additional_monthly_interest_rate_list, initial_value)
        cumulative_interest_value_list = [sum(values) for values in zip(cumulative_interest_value_list, additional_cumulative_interest_value_list)]
        cumulative_monthly_interest_rate_list = self.InterestCalculation.getCumulativeInterestRateList(cumulative_interest_value_list, initial_value)
        final_value = initial_value + self.InterestCalculation.calculateInterestValue(cumulative_monthly_interest_rate_list, initial_value)
        return final_value, cumulative_interest_value_list, cumulative_monthly_interest_rate_list

    def sumValuesPerProportionalInterestRate(self, initial_value, cumulative_interest_value_list):
        cumulative_interest_value_list = [value*self.ParameterWidget.getAdditionalInterestRate() for value in cumulative_interest_value_list]
        cumulative_monthly_interest_rate_list = self.InterestCalculation.getCumulativeInterestRateList(cumulative_interest_value_list, initial_value)
        final_value = initial_value + self.InterestCalculation.calculateInterestValue(cumulative_monthly_interest_rate_list, initial_value)
        return final_value, cumulative_interest_value_list, cumulative_monthly_interest_rate_list

    def onCalculateClick(self):
        inital_period, final_period = self.ParameterWidget.getSelectedPeriod()
        initial_value = self.ParameterWidget.getInitialValue()
        filtered_dataframe = self.DataframeFilter.filterDataframePerPeriod(self.stacked_dataframe, 'Data Ajustada', inital_period, final_period)
        monthly_interest_rate_list = self.DataframeFilter.getListFromDataframeColumn(filtered_dataframe, 'Taxa Mensal')
        period_list = self.DataframeFilter.getListFromDataframeColumn(filtered_dataframe, 'Data Ajustada')
        if self.ParameterWidget.isValidSelectedPeriod():
            values_tuple = self.calculateValuesPerIndexerCurve(initial_value, monthly_interest_rate_list)
            final_value = values_tuple[0]
            cumulative_interest_value_list = values_tuple[1]
            cumulative_monthly_interest_rate_list = values_tuple[2]
            if self.ParameterWidget.isAdditionalRatePrefixed():
                values_tuple = self.sumValuesPerPrefixedInterestRate(initial_value, monthly_interest_rate_list, cumulative_interest_value_list)
                final_value = values_tuple[0]
                cumulative_interest_value_list = values_tuple[1]
                cumulative_monthly_interest_rate_list = values_tuple[2]
            elif self.ParameterWidget.isAdditionalRateProportional():
                values_tuple = self.sumValuesPerProportionalInterestRate(initial_value, cumulative_interest_value_list)
                final_value = values_tuple[0]
                cumulative_interest_value_list = values_tuple[1]
                cumulative_monthly_interest_rate_list = values_tuple[2]
            print('Dados de entrada:')
            print(' - Indicador Econômico:', self.indexer_name)
            print(' - Montante inicial:', TreeviewValueFormat.setCurrencyFormat(initial_value))
            print(' - Período total em meses:', len(period_list))
            print(' - Taxa Adicional:', TreeviewValueFormat.setPercentageFormat(self.ParameterWidget.getAdditionalInterestRate()))
            print(' - Tipo:', self.ParameterWidget.getAdditionalInterestRateTypeString())
            print('Valores brutos:')
            print(' - Montante final:', TreeviewValueFormat.setCurrencyFormat(final_value))
            print(' - Valor de Juros total:', TreeviewValueFormat.setCurrencyFormat(self.InterestCalculation.calculateInterestValueByValues(initial_value, final_value)))
            print(' - Taxa de Juros total:', TreeviewValueFormat.setPercentageFormat(self.InterestCalculation.calculateInterestRateByValues(initial_value, final_value)))
            print('')
            # print('\nValor de Juros mensal (R$):\n', cumulative_interest_value_list)
            # print('\nTaxa de Juros mensal (%):\n', cumulative_monthly_interest_rate_list)
            # print('\nLista de meses:', period_list)
        else:
            print('O período selecionado é inválido. Por favor, selecione um \'Período Final\' maior ou igual ao \'Período Inicial\'.\n')

    def setMonthsItems(self, months_list):
        months_list = [str(month) for month in months_list]
        self.ParameterWidget.setMonthsItems(months_list)
    
    def setYearsItems(self, years_list):
        years_list = [str(year) for year in years_list]
        self.ParameterWidget.setYearsItems(years_list)

    def setDefaultValues(self, indexer_name):
        if ('IPCA' in indexer_name):
            self.ParameterWidget.setDefaultValues(1)
        elif ('CDI' in indexer_name) or ('SELIC' in indexer_name):
            self.ParameterWidget.setDefaultValues(2)
        else:
            self.ParameterWidget.setDefaultValues(0)


class EconomicIndexerWidget:

    """ 
    This class is used to create a special widget for user input related to some Economic Indexer.

    Basically, we have a set of tabs with several types of Economic Indexers (IPCA, SELIC, etc.), including:
    - a widget to enter some data and perform some calculation/plotting graphs
    - a treeview table

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    """

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
            dataframe = self.Indexers.__getattribute__(indexer_name).getDataframe(stacked=True)
            formated_dataframe = self.Indexers.__getattribute__(indexer_name).getFormatedDataframe(stacked=False)
            coordinate_X = Window.DEFAULT_BORDER_SIZE
            coordinate_Y = Window.DEFAULT_BORDER_SIZE
            width = EconomicIndexerWidget.TAB_WIDTH_USEFUL
            indexer_panel = IndexerPanelWidget(tab_central_widget, indexer_name, dataframe, formated_dataframe, coordinate_X=coordinate_X, coordinate_Y=coordinate_Y, width=width)
            indexer_panel.setMonthsItems(self.Indexers.__getattribute__(indexer_name).getMonthsList())
            indexer_panel.setYearsItems(self.Indexers.__getattribute__(indexer_name).getYearsList())
            indexer_panel.setDefaultValues(indexer_name)
