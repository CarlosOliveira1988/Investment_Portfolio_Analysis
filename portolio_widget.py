from window import Window
from treeview import Treeview
from gui_lib.pushbutton import StandardPushButton


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
        self.__PushButton = StandardPushButton(CentralWidget, ExpandCollapsePushButton.EXPAND_TEXT, 
        coordinate_X=(Treeview.DEFAULT_WIDTH + 2*Window.DEFAULT_BORDER_SIZE), 
        coordinate_Y=(Window.DEFAULT_BORDER_SIZE), 
        onClickMethod=self.__expandCollapseAll)

        # Connect events
        self.__expandEvent = onExpandMethod
        self.__collapseEvent = onCollapseMethod

        # Initial state
        self.collapseAll()

    """
    Private methods
    """
    def __expandCollapseAll(self):
        if self.__IsExpandedFlag:
            self.collapseAll()
        else:
            self.expandAll()

    """
    Public methods
    """
    def expandAll(self):
        self.__IsExpandedFlag = True
        self.__PushButton.setText(ExpandCollapsePushButton.COLLAPSE_TEXT)
        self.__expandEvent()

    def collapseAll(self):
        self.__IsExpandedFlag = False
        self.__PushButton.setText(ExpandCollapsePushButton.EXPAND_TEXT)
        self.__collapseEvent()


class PortfolioViewerWidget:
    """ 
    This class is used to create a special widget for portfolio visualization.

    Basically, it has a 'table' and a 'expand/collapse lines push button'.

    Arguments:
    - CentralWidget: the widget where the push button will be placed
    - columns_title_list: a list of columns titles
    """
    def __init__(self, CentralWidget, columns_title_list):
        self.__PortolioTreeview = Treeview(CentralWidget, columns_title_list)
        self.__ExpandCollapsePushButton = ExpandCollapsePushButton(CentralWidget, self.__expandAllLines, self.__collapseAllLines)
        self.__resizeColumns()

    """
    Private methods
    """
    def __resizeColumns(self):
        self.__ExpandCollapsePushButton.expandAll()
        self.__PortolioTreeview.resizeColumnsToContents()
        self.__ExpandCollapsePushButton.collapseAll()

    def __expandAllLines(self):
        self.__PortolioTreeview.expandParentLines()
    
    def __collapseAllLines(self):
        self.__PortolioTreeview.collapseParentLines()

    """
    Public methods
    """
    def getTreeview(self):
        return self.__PortolioTreeview
