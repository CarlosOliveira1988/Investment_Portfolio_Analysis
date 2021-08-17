from PyQt5 import QtWidgets


class Window(QtWidgets.QMainWindow):
    """
    This class provides methods and attributes to create a window.

    Arguments:
    - window_title: the title of the window
    """

    # Contants related to the window
    DEFAULT_WIDTH = 1200
    DEFAULT_HEIGHT = 675
    DEFAULT_BORDER_SIZE = 20

    def __init__(self, window_title):
        super().__init__()
        self.__setupWindow(window_title)
        self.__setDefaultWindowSize()

    """
    Private methods
    """

    def __setupWindow(self, window_title):
        self.CentralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.CentralWidget)
        self.setWindowTitle(window_title)

    def __setDefaultWindowSize(self):
        self.CentralWidget.resize(Window.DEFAULT_WIDTH, Window.DEFAULT_HEIGHT)
        self.resize(Window.DEFAULT_WIDTH, Window.DEFAULT_HEIGHT)

    """
    Public methods
    """

    def getCentralWidget(self):
        """
        Returns the central widget of the window.

        All GUI components (buttons, checkboxes, tables, etc.) must have this widget as argument.
        """
        return self.CentralWidget
