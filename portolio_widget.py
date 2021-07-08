from PyQt5 import QtWidgets
from PyQt5 import QtCore

from window import Window
from treeview import Treeview


class PushButton:
    """ 
    This class is used to create a Standard Push Button.

    Arguments:
    - CentralWidget: the widget where the push button will be placed
    - title: the text on the button
    - coordinate_X: the window X coordinate where the PushButton will be placed
    - coordinate_Y: the window Y coordinate where the PushButton will be placed
    - width: the width of the PushButton
    - height: the height of the PushButton
    - onClickMethod: the callback method of the "onClick" event
    """

    # Contants related to the push button
    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 20

    def __init__(self, CentralWidget, title, coordinate_X=0, coordinate_Y=0, 
    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, onClickMethod=None):
        self.PushButton = QtWidgets.QPushButton(CentralWidget)
        self.PushButton.setGeometry(QtCore.QRect(coordinate_X, coordinate_Y, width, height))
        self.PushButton.setText(title)
        self.PushButton.clicked.connect(onClickMethod)

    """
    Public methods
    """
    def setTitle(self, title):
        self.PushButton.setText(title)


class ExpandCollapsePushButton:
    """ 
    This class is used to create a special push button for expanding and collapsing lines in a table.

    Arguments:
    - CentralWidget: the widget where the push button will be placed
    - onExpandMethod: the callback method called to "expand" the lines in a table
    - onCollapseMethod: the callback method called to "collapse" the lines in a table
    """

    # Contants related to the special push button
    EXPAND_TEXT = 'Expand all lines'
    COLLAPSE_TEXT = 'Collapse all lines'

    def __init__(self, CentralWidget, onExpandMethod=None, onCollapseMethod=None):
        # Push button
        self.PushButton = PushButton(CentralWidget, ExpandCollapsePushButton.EXPAND_TEXT, 
        coordinate_X=(Treeview.DEFAULT_WIDTH + 2*Window.DEFAULT_BORDER_SIZE), 
        coordinate_Y=(Window.DEFAULT_BORDER_SIZE), 
        onClickMethod=self.__expandCollapseAll)

        # Connect events
        self.expandEvent = onExpandMethod
        self.collapseEvent = onCollapseMethod

        # Initial state
        self.__collapseAll()

    """
    Private methods
    """
    def __expandAll(self):
        self.IsExpandedFlag = True
        self.PushButton.setTitle(ExpandCollapsePushButton.COLLAPSE_TEXT)
        self.expandEvent()

    def __collapseAll(self):
        self.IsExpandedFlag = False
        self.PushButton.setTitle(ExpandCollapsePushButton.EXPAND_TEXT)
        self.collapseEvent()

    def __expandCollapseAll(self):
        if self.IsExpandedFlag:
            self.__collapseAll()
        else:
            self.__expandAll()


class PortfolioViewerWidget:
    """ 
    This class is used to create a special widget for portfolio visualization.

    Basically, it has a 'table' and a 'expand/collapse lines push button'.

    Arguments:
    - CentralWidget: the widget where the push button will be placed
    - columns_title_list: a list of columns titles
    """
    def __init__(self, CentralWidget, columns_title_list):
        self.PortolioTreeview = Treeview(CentralWidget, columns_title_list)
        self.ExpandCollapsePushButton = ExpandCollapsePushButton(CentralWidget, self.__expandAllLines, self.__collapseAllLines)

    """
    Private methods
    """
    def __expandAllLines(self):
        self.PortolioTreeview.expandParentLines()
    
    def __collapseAllLines(self):
        self.PortolioTreeview.collapseParentLines()

    """
    Public methods
    """
    def getTreeview(self):
        return self.PortolioTreeview
