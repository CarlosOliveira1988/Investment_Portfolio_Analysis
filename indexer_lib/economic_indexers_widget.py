from datetime import datetime

from gui_lib.combobox import StandardComboBox
from gui_lib.pushbutton import StandardPushButton
from gui_lib.tab import StandardTab
from gui_lib.textedit import StandardTextEdit
from gui_lib.treeview.treeview_format import TreeviewValueFormat
from gui_lib.treeview.treeview_pandas import TreeviewPandas
from gui_lib.window import Window
from matplotlib import pyplot as plt
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMessageBox
from widget_lib.date_combobox import DateComboBox
from widget_lib.parameter_lineedit import ParameterLineEdit
from widget_lib.widget_interface import WidgetInterface

from indexer_lib.economic_indexers import EconomicIndexer
from indexer_lib.interest_calculation import (
    InterestOnCurve,
    InterestOnCurvePrefixed,
    InterestOnCurveProportional,
)


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

    ADDITIONAL_RATE_NONE = "Nenhum    "
    ADDITIONAL_RATE_NONE_INDEX = 0
    ADDITIONAL_RATE_NONE_DEFAULT = "0,00"

    ADDITIONAL_RATE_PREFIXED = "Préfixado (+)"
    ADDITIONAL_RATE_PREFIXED_INDEX = 1
    ADDITIONAL_RATE_PREFIXED_DEFAULT = "0,00"

    ADDITIONAL_RATE_PROPORTIONAL = "Proporcional (x)"
    ADDITIONAL_RATE_PROPORTIONAL_INDEX = 2
    ADDITIONAL_RATE_PROPORTIONAL_DEFAULT = "100,00"

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

        # ParameterLineEdit
        self.ParameterLineEdit = ParameterLineEdit(
            self, title, coordinate_Y=self.getInternalHeight(), width=width
        )
        self.ParameterLineEditValidator = QtGui.QDoubleValidator(
            bottom=0.00,
            top=100.00,
            decimals=2,
        )
        self.ParameterLineEditValidator.setNotation(
            QtGui.QDoubleValidator.StandardNotation,
        )
        self.ParameterLineEdit.LineEdit.setValidator(
            self.ParameterLineEditValidator,
        )
        self.incrementInternalHeight(self.ParameterLineEdit.height())

        # ComboBox
        self.StandardComboBox = StandardComboBox(
            self, coordinate_Y=self.getInternalHeight(), width=width
        )
        self.StandardComboBox.addItem(InterestRateSelection.ADDITIONAL_RATE_NONE)
        self.StandardComboBox.addItem(InterestRateSelection.ADDITIONAL_RATE_PREFIXED)
        self.StandardComboBox.addItem(
            InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL
        )
        self.incrementInternalHeight(self.StandardComboBox.height())

        # Widget dimensions
        self.setGeometry(
            QtCore.QRect(coordinate_X, coordinate_Y, width, self.getInternalHeight())
        )

    """
    Puclic methods
    """

    def isAdditionalRateNone(self):
        return (
            self.StandardComboBox.currentIndex()
            == InterestRateSelection.ADDITIONAL_RATE_NONE_INDEX
        )

    def isAdditionalRatePrefixed(self):
        return (
            self.StandardComboBox.currentIndex()
            == InterestRateSelection.ADDITIONAL_RATE_PREFIXED_INDEX
        )

    def isAdditionalRateProportional(self):
        return (
            self.StandardComboBox.currentIndex()
            == InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL_INDEX
        )

    def setDefaultValues(self, default_type_number=ADDITIONAL_RATE_NONE_INDEX):
        if default_type_number == InterestRateSelection.ADDITIONAL_RATE_NONE_INDEX:
            self.ParameterLineEdit.LineEdit.setText(
                InterestRateSelection.ADDITIONAL_RATE_NONE_DEFAULT
            )
            self.StandardComboBox.setCurrentIndex(
                InterestRateSelection.ADDITIONAL_RATE_NONE_INDEX
            )
        elif (
            default_type_number == InterestRateSelection.ADDITIONAL_RATE_PREFIXED_INDEX
        ):
            self.ParameterLineEdit.LineEdit.setText(
                InterestRateSelection.ADDITIONAL_RATE_PREFIXED_DEFAULT
            )
            self.StandardComboBox.setCurrentIndex(
                InterestRateSelection.ADDITIONAL_RATE_PREFIXED_INDEX
            )
        elif (
            default_type_number
            == InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL_INDEX
        ):
            self.ParameterLineEdit.LineEdit.setText(
                InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL_DEFAULT
            )
            self.StandardComboBox.setCurrentIndex(
                InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL_INDEX
            )

    def getAdditionalInterestRate(self):
        interest_rate_value = self.ParameterLineEdit.LineEdit.text()
        interest_rate_value = interest_rate_value.replace(",", ".")
        try:
            return float(interest_rate_value) / 100
        except ValueError:
            return ""

    def getAdditionalInterestRateTypeString(self):
        selected_text = self.StandardComboBox.currentText()
        if selected_text == InterestRateSelection.ADDITIONAL_RATE_NONE:
            selected_type = InterestRateSelection.ADDITIONAL_RATE_NONE
        else:
            selected_type = (
                TreeviewValueFormat.setPercentageFormat(
                    self.getAdditionalInterestRate()
                )
                + " "
                + selected_text[:-4]
            )
        return selected_type


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

    INITIAL_VALUE_LABEL = "Valor Inicial (R$)"
    INITIAL_PERIOD_LABEL = "Período Inicial"
    FINAL_PERIOD_LABEL = "Período Final"
    ADDITIONAL_INTEREST_RATE_LABEL = "Taxa Adicional (%)"
    CALCULATE_BUTTON_LABEL = "Calcular"
    PLOT_BUTTON_LABEL = "Gráfico"

    INITIAL_VALUE_DEFAULT = "1000,00"

    def __init__(
        self,
        CentralWidget,
        coordinate_X=0,
        coordinate_Y=0,
        onCalculateClick=None,
        onPlotClick=None,
    ):
        # Internal central widget
        super().__init__(CentralWidget)

        # Initial Value
        self.InitialValue = ParameterLineEdit(
            self,
            ParameterWidget.INITIAL_VALUE_LABEL,
            coordinate_Y=self.getInternalHeight(),
            width=ParameterWidget.WIDTH,
        )
        self.InitialValueValidator = QtGui.QDoubleValidator(
            bottom=0.01,
            top=100000000.00,
            decimals=2,
        )
        self.InitialValueValidator.setNotation(
            QtGui.QDoubleValidator.StandardNotation,
        )
        self.InitialValue.LineEdit.setValidator(
            self.InitialValueValidator,
        )
        self.incrementInternalHeight(
            self.InitialValue.height() + ParameterWidget.EMPTY_SPACE
        )

        # Initial Period selection
        self.InitialPeriod = DateComboBox(
            self,
            ParameterWidget.INITIAL_PERIOD_LABEL,
            coordinate_Y=self.getInternalHeight(),
            width=ParameterWidget.WIDTH,
        )
        self.incrementInternalHeight(
            self.InitialPeriod.height() + ParameterWidget.EMPTY_SPACE
        )

        # Final Period selection
        self.FinalPeriod = DateComboBox(
            self,
            ParameterWidget.FINAL_PERIOD_LABEL,
            coordinate_Y=self.getInternalHeight(),
            width=ParameterWidget.WIDTH,
        )
        self.incrementInternalHeight(
            self.FinalPeriod.height() + ParameterWidget.EMPTY_SPACE
        )

        # Additional Interest Rate
        self.InterestRate = InterestRateSelection(
            self,
            ParameterWidget.ADDITIONAL_INTEREST_RATE_LABEL,
            coordinate_Y=self.getInternalHeight(),
            width=ParameterWidget.WIDTH,
        )
        self.incrementInternalHeight(
            self.InterestRate.height() + ParameterWidget.EMPTY_SPACE
        )

        # Calculate button
        self.Calculate = StandardPushButton(
            self,
            ParameterWidget.CALCULATE_BUTTON_LABEL,
            coordinate_Y=self.getInternalHeight(),
            width=ParameterWidget.WIDTH,
            onClickMethod=onCalculateClick,
        )
        self.incrementInternalHeight(
            self.Calculate.height() + ParameterWidget.EMPTY_SPACE
        )

        # Plot button
        self.Plot = StandardPushButton(
            self,
            ParameterWidget.PLOT_BUTTON_LABEL,
            coordinate_Y=self.getInternalHeight(),
            width=ParameterWidget.WIDTH,
            onClickMethod=onPlotClick,
        )
        self.incrementInternalHeight(self.Plot.height() + ParameterWidget.EMPTY_SPACE)

        # Widget dimensions
        self.setGeometry(
            QtCore.QRect(
                coordinate_X,
                coordinate_Y,
                ParameterWidget.WIDTH,
                self.getInternalHeight(),
            )
        )

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

    def __getInitialValueText(self):
        initial_value = self.InitialValue.LineEdit.text()
        return initial_value.replace(",", ".")

    def getInitialValue(self):
        text_value = self.__getInitialValueText()
        try:
            return float(text_value)
        except ValueError:
            return None

    def isValidInitialValue(self):
        value = self.getInitialValue()
        return type(value) == float or type(value) == int

    def getAdditionalInterestRate(self):
        return self.InterestRate.getAdditionalInterestRate()

    def isValidAdditionalInterestRate(self):
        value = self.getAdditionalInterestRate()
        return type(value) == float or type(value) == int

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
    - height: the height of the widget
    """

    EMPTY_SPACE = StandardComboBox.DEFAULT_HEIGHT

    def __init__(
        self,
        CentralWidget,
        ResultsWidget,
        indexer_name,
        stacked_dataframe,
        formated_dataframe,
        coordinate_X,
        coordinate_Y,
        width,
        height,
    ):
        # Internal central widget
        super().__init__(CentralWidget)

        # ParameterWidget
        self.ParameterWidget = ParameterWidget(
            self,
            coordinate_X=self.getInternalWidth(),
            coordinate_Y=0,
            onCalculateClick=self.__onCalculateClick,
            onPlotClick=self.__onPlotClick,
        )
        self.incrementInternalWidth(
            self.ParameterWidget.width() + IndexerPanelWidget.EMPTY_SPACE
        )

        # TreeviewPandas
        self.TreeviewPandas = TreeviewPandas(
            self,
            formated_dataframe,
            coordinate_X=self.getInternalWidth(),
            coordinate_Y=0,
            width=width - self.getInternalWidth(),
            height=height,
        )
        self.TreeviewPandas.showPandas()
        self.TreeviewPandas.resizeColumnsToTreeViewWidth()
        self.incrementInternalWidth(self.TreeviewPandas.width())

        # Auxiliary variables
        from indexer_lib.dataframe_filter import DataframeFilter
        from indexer_lib.indexer_manager import StackedFormatConstants
        from indexer_lib.interest_calculation import Benchmark

        self.ResultsWidget = ResultsWidget
        self.Benchmark = Benchmark()
        self.StackedFormatConstants = StackedFormatConstants()
        self.DataframeFilter = DataframeFilter()
        self.indexer_name = indexer_name
        self.stacked_dataframe = stacked_dataframe
        self.inital_period = None
        self.final_period = None
        self.period_list = []
        self.initial_value = 0
        self.interest_value = 0
        self.interest_rate = 0
        self.final_value = 0
        self.additional_interest_rate = 0
        self.monthly_interest_rate_list = []
        self.cumulative_interest_value_list = []
        self.cumulative_monthly_interest_rate_list = []

        # Widget dimensions
        self.setGeometry(
            QtCore.QRect(coordinate_X, coordinate_Y, self.getInternalWidth(), height)
        )

    """
    Private methods
    """

    def __getUserWidgetValues(self):
        self.inital_period, self.final_period = self.ParameterWidget.getSelectedPeriod()
        self.initial_value = self.ParameterWidget.getInitialValue()
        filtered_dataframe = self.DataframeFilter.filterDataframePerPeriod(
            self.stacked_dataframe,
            self.StackedFormatConstants.getAdjustedDateTitle(),
            self.inital_period,
            self.final_period,
        )
        self.monthly_interest_rate_list = (
            self.DataframeFilter.getListFromDataframeColumn(
                filtered_dataframe, self.StackedFormatConstants.getInterestTitle()
            )
        )
        self.period_list = self.DataframeFilter.getListFromDataframeColumn(
            filtered_dataframe, self.StackedFormatConstants.getAdjustedDateTitle()
        )
        self.additional_interest_rate = self.ParameterWidget.getAdditionalInterestRate()
        self.additional_interest_rate_string = (
            self.ParameterWidget.getAdditionalInterestRateTypeString()
        )

    def __calculate(self, InterestOnCurveObject):
        InterestOnCurveObject.calculateValues()
        self.final_value = InterestOnCurveObject.getFinalValue()
        self.interest_value = InterestOnCurveObject.getInterestValue()
        self.interest_rate = InterestOnCurveObject.getInterestRate()
        self.cumulative_interest_value_list = (
            InterestOnCurveObject.getInterestValueList()
        )
        self.cumulative_monthly_interest_rate_list = (
            InterestOnCurveObject.getInterestRateList()
        )
        self.Benchmark.setValues(self.initial_value, self.final_value)
        self.Benchmark.setPeriods(self.inital_period, self.final_period)
        self.Benchmark.setTotalMonths(len(self.period_list))

    def __showResults(self):
        self.ResultsWidget.addResult("")
        self.ResultsWidget.addResult(
            "Estudo " + TreeviewValueFormat.setDateTimeFormat(datetime.now())
        )
        self.ResultsWidget.addResult("")
        self.ResultsWidget.addResult("Dados de entrada: ")
        self.ResultsWidget.addResult(
            " - Montante inicial: "
            + TreeviewValueFormat.setCurrencyFormat(self.initial_value)
        )
        self.ResultsWidget.addResult(
            " - Período inicial: "
            + TreeviewValueFormat.setDateFormat(self.inital_period)
        )
        self.ResultsWidget.addResult(
            " - Período final: " + TreeviewValueFormat.setDateFormat(self.final_period)
        )
        self.ResultsWidget.addResult(
            " - Período total em meses: " + str(len(self.period_list))
        )
        self.ResultsWidget.addResult(" - Indicador de referência: " + self.indexer_name)
        self.ResultsWidget.addResult(
            " - Taxa adicional: "
            + TreeviewValueFormat.setPercentageFormat(
                self.additional_interest_rate_string
            )
        )
        self.ResultsWidget.addResult("")
        self.ResultsWidget.addResult("Resultado final: ")
        self.ResultsWidget.addResult(
            " - Montante final: "
            + TreeviewValueFormat.setCurrencyFormat(self.final_value)
        )
        self.ResultsWidget.addResult(
            " - Taxa de juros total: "
            + TreeviewValueFormat.setPercentageFormat(self.interest_rate)
        )
        self.ResultsWidget.addResult(
            " - Valor de juros total: "
            + TreeviewValueFormat.setCurrencyFormat(self.interest_value)
        )
        self.ResultsWidget.addResult("")
        self.ResultsWidget.addResult("Benchmarking: ")
        self.ResultsWidget.addResult(
            " - Equivalente mensal:"
            + TreeviewValueFormat.setPercentageFormat(
                self.Benchmark.getMonthlyEquivalentInterestRate()
            )
        )
        self.ResultsWidget.addResult(
            " - Equivalente anual: "
            + TreeviewValueFormat.setPercentageFormat(
                self.Benchmark.getYearlyEquivalentInterestRate()
            )
        )
        self.ResultsWidget.addResult(
            " - Equivalente Pós x CDI anual: "
            + TreeviewValueFormat.setPercentageFormat(
                self.Benchmark.getCDIEquivalentInterestRate()
            )
        )
        self.ResultsWidget.addResult(
            " - Equivalente Pré + IPCA anual: "
            + TreeviewValueFormat.setPercentageFormat(
                self.Benchmark.getIPCAEquivalentInterestRate()
            )
        )
        self.ResultsWidget.addResult("")
        self.ResultsWidget.addResult("-----------------------------------------------")

    def __isValidParameters(self):
        # Only one failure messagebox will be displayed per attempt

        valid_flag = True

        # Initial Value
        if self.ParameterWidget.isValidInitialValue() and valid_flag == True:
            pass
        elif valid_flag:
            valid_flag = False
            msg = "O valor do campo 'Valor Inicial' é inválido."
            QMessageBox.warning(self, "Indicadores Econômicos", msg, QMessageBox.Ok)

        # Initial and Final periods
        if self.ParameterWidget.isValidSelectedPeriod():
            pass
        elif valid_flag:
            valid_flag = False
            msg = "O período selecionado é inválido. Selecione um 'Período Final' maior ou igual ao 'Período Inicial'."
            QMessageBox.warning(self, "Indicadores Econômicos", msg, QMessageBox.Ok)

        # Additional Interest Rate
        if self.ParameterWidget.isValidAdditionalInterestRate() and valid_flag == True:
            pass
        elif valid_flag:
            valid_flag = False
            msg = "O valor do campo 'Taxa Adicional' é inválido."
            QMessageBox.warning(self, "Indicadores Econômicos", msg, QMessageBox.Ok)

        return valid_flag

    def __onCalculateClick(self):
        successful_flag = False
        self.__getUserWidgetValues()
        if self.__isValidParameters():
            if self.ParameterWidget.isAdditionalRateNone():
                InterestOnCurveObject = InterestOnCurve(
                    self.initial_value, self.monthly_interest_rate_list
                )
            elif self.ParameterWidget.isAdditionalRatePrefixed():
                InterestOnCurveObject = InterestOnCurvePrefixed(
                    self.initial_value,
                    self.monthly_interest_rate_list,
                    self.additional_interest_rate,
                )
            elif self.ParameterWidget.isAdditionalRateProportional():
                InterestOnCurveObject = InterestOnCurveProportional(
                    self.initial_value,
                    self.monthly_interest_rate_list,
                    self.additional_interest_rate,
                )
            self.__calculate(InterestOnCurveObject)
            self.__showResults()
            successful_flag = True
        return successful_flag

    def __showPlot(
        self,
        subplot_row,
        subplot_col,
        subplot_axs,
        x_list,
        y_list,
        x_label,
        y_label,
        plot_label,
        plot_window_title,
    ):
        # Custom information
        subplot_axs[subplot_row, subplot_col].plot(x_list, y_list, label=plot_label)
        subplot_axs[subplot_row, subplot_col].set_title(plot_window_title)
        subplot_axs[subplot_row, subplot_col].set(xlabel=x_label, ylabel=y_label)

        # Common information
        subplot_axs[subplot_row, subplot_col].legend(title="Referente ao:")
        subplot_axs[subplot_row, subplot_col].grid()

    def __getAccumulatedValueList(self, initial_value, interest_value_list):
        value = initial_value
        value_list = []
        for interest_value in interest_value_list:
            value += interest_value
            value_list.append(value)
        return value_list

    def __onPlotClick(self):
        if self.__onCalculateClick():
            plt.close()
            fig, axs = plt.subplots(2, 2)

            value_list = self.__getAccumulatedValueList(
                self.initial_value, self.cumulative_interest_value_list
            )
            self.__showPlot(
                0,
                0,
                axs,
                self.period_list,
                value_list,
                "Meses",
                "Valor total (R$)",
                "Valor aportado",
                "Valor total acumulado (R$)",
            )

            value_list = self.__getAccumulatedValueList(
                0, self.cumulative_interest_value_list
            )
            self.__showPlot(
                0,
                1,
                axs,
                self.period_list,
                value_list,
                "Meses",
                "Valor total (R$)",
                "Valor aportado",
                "Valor de juros acumulado (R$)",
            )

            self.__showPlot(
                1,
                0,
                axs,
                self.period_list,
                self.cumulative_interest_value_list,
                "Meses",
                "Valor total (R$)",
                "Valor aportado",
                "Valor de juros mensal (R$)",
            )

            adjusted_list = [
                100 * rate for rate in self.cumulative_monthly_interest_rate_list
            ]
            self.__showPlot(
                1,
                1,
                axs,
                self.period_list,
                adjusted_list,
                "Meses",
                "Taxa (%)",
                "Valor aportado",
                "Taxa de juros mensal (%)",
            )

            fig.tight_layout()
            plt.show()
            plt.gcf().canvas.set_window_title("Gráfico")

    """
    Puclic methods
    """

    def setMonthsItems(self, months_list):
        months_list = [str(month) for month in months_list]
        self.ParameterWidget.setMonthsItems(months_list)

    def setYearsItems(self, years_list):
        years_list = [str(year) for year in years_list]
        self.ParameterWidget.setYearsItems(years_list)

    def setDefaultValues(self, indexer_name):
        if "IPCA" in indexer_name:
            self.ParameterWidget.setDefaultValues(
                InterestRateSelection.ADDITIONAL_RATE_PREFIXED_INDEX
            )
        elif ("CDI" in indexer_name) or ("SELIC" in indexer_name):
            self.ParameterWidget.setDefaultValues(
                InterestRateSelection.ADDITIONAL_RATE_PROPORTIONAL_INDEX
            )
        else:
            self.ParameterWidget.setDefaultValues(
                InterestRateSelection.ADDITIONAL_RATE_NONE_INDEX
            )


class ResultsWidget(WidgetInterface):

    CLEAR_BUTTON_TEXT = "Limpar resultados"

    RESULTS_WIDTH = 250

    EMPTY_SPACE = StandardPushButton.DEFAULT_HEIGHT

    def __init__(
        self,
        CentralWidget,
        coordinate_X=0,
        coordinate_Y=0,
        width=RESULTS_WIDTH,
        height=StandardTextEdit.DEFAULT_HEIGHT,
    ):
        # Internal central widget
        super().__init__(CentralWidget)

        # Define initial dimensions
        total_height = height
        button_height = StandardPushButton.DEFAULT_HEIGHT
        text_height = total_height - 2 * ResultsWidget.EMPTY_SPACE - button_height

        # Text results
        self.TextResult = StandardTextEdit(self, width=width, height=text_height)
        self.incrementInternalWidth(self.TextResult.width())
        self.incrementInternalHeight(
            self.TextResult.height() + ResultsWidget.EMPTY_SPACE
        )

        # Clear button
        self.Clear = StandardPushButton(
            self,
            ResultsWidget.CLEAR_BUTTON_TEXT,
            coordinate_Y=self.getInternalHeight(),
            width=width,
            height=button_height,
            onClickMethod=self.__clearResults,
        )
        self.incrementInternalHeight(self.TextResult.height())

        # Widget dimensions
        self.setGeometry(
            QtCore.QRect(
                coordinate_X,
                coordinate_Y,
                self.getInternalWidth(),
                self.getInternalHeight(),
            )
        )

    def __clearResults(self):
        self.TextResult.clear()

    def addResult(self, text):
        self.TextResult.moveCursor(QTextCursor.End)
        self.TextResult.insertPlainText(text + "\n")


class EconomicIndexerWidget(WidgetInterface):

    """
    This class is used to create a special widget for user input related to some Economic Indexer.

    Basically, we have a set of tabs with several types of Economic Indexers (IPCA, SELIC, etc.), including:
    - a widget to enter some data and perform some calculation/plotting graphs
    - a treeview table

    Arguments:
    - CentralWidget: the widget where all the components will be placed
    """

    EMPTY_SPACE = Window.DEFAULT_BORDER_SIZE
    TAB_WIDTH = 1070
    TAB_HEIGHT = 500
    TAB_WIDTH_USEFUL = TAB_WIDTH - 2 * EMPTY_SPACE
    TAB_HEIGHT_USEFUL = TAB_HEIGHT - 3 * EMPTY_SPACE

    def __init__(self, CentralWidget, coordinate_X=0, coordinate_Y=0):
        # Internal central widget
        super().__init__(CentralWidget)

        # Economic indexers (IPCA, SELIC, etc.)
        self.Indexers = EconomicIndexer()

        # Tab panel widget
        self.TabPanel = StandardTab(
            CentralWidget,
            width=EconomicIndexerWidget.TAB_WIDTH,
            height=EconomicIndexerWidget.TAB_HEIGHT,
        )
        self.incrementInternalWidth(
            self.TabPanel.width() + EconomicIndexerWidget.EMPTY_SPACE
        )
        self.incrementInternalHeight(
            self.TabPanel.height() + EconomicIndexerWidget.EMPTY_SPACE
        )

        # Results widget
        self.Results = ResultsWidget(
            CentralWidget,
            coordinate_X=self.getInternalWidth(),
            coordinate_Y=EconomicIndexerWidget.EMPTY_SPACE,
        )
        self.incrementInternalWidth(
            self.Results.width() + EconomicIndexerWidget.EMPTY_SPACE
        )

        # Tab panel widget
        self.__addIndexerPanels()

        # Widget dimensions
        self.setGeometry(
            QtCore.QRect(
                coordinate_X,
                coordinate_Y,
                self.getInternalWidth(),
                self.getInternalHeight(),
            )
        )

    def __addIndexerPanels(self):
        for indexer_name in self.Indexers.getNamesList():
            tab_central_widget = self.TabPanel.addNewTab(indexer_name)
            dataframe = self.Indexers.__getattribute__(indexer_name).getDataframe(
                stacked=True
            )
            formated_dataframe = self.Indexers.__getattribute__(
                indexer_name
            ).getFormatedDataframe(stacked=False)
            coordinate_X = Window.DEFAULT_BORDER_SIZE
            coordinate_Y = Window.DEFAULT_BORDER_SIZE
            width = EconomicIndexerWidget.TAB_WIDTH_USEFUL
            height = EconomicIndexerWidget.TAB_HEIGHT_USEFUL
            indexer_panel = IndexerPanelWidget(
                tab_central_widget,
                self.Results,
                indexer_name,
                dataframe,
                formated_dataframe,
                coordinate_X=coordinate_X,
                coordinate_Y=coordinate_Y,
                width=width,
                height=height,
            )
            indexer_panel.setMonthsItems(
                self.Indexers.__getattribute__(indexer_name).getMonthsList()
            )
            indexer_panel.setYearsItems(
                self.Indexers.__getattribute__(indexer_name).getYearsList()
            )
            indexer_panel.setDefaultValues(indexer_name)
