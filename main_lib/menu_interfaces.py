"""This file has some classes to work with menus creation."""

from PyQt5 import QtWidgets


class SubMenu(QtWidgets.QMenu):
    """SubMenu class for menus creation."""

    def __init__(self, tag_menu, menu_bar, function):
        """Create the SubMenu object."""
        super().__init__(tag_menu, menu_bar)
        self.action = self.setAction(tag_menu, function)

    def setAction(self, menu_tag, function):
        """Set the related 'Action' to a specific 'menu'."""
        action = QtWidgets.QAction(menu_tag)
        action.triggered.connect(function)
        return action

    def getAction(self):
        """Return the 'Action'."""
        return self.action


class MenuInterface(QtWidgets.QMenu):
    """Interface to used while creating new menus for the application."""

    def __init__(self, menu_title, menu_bar):
        """Create the MenuInterface object."""
        super().__init__(menu_title, menu_bar)

    def addSubmenu(self, submenu_title, submenu_function):
        """Create the sub menu item."""
        sub_menu = SubMenu(
            submenu_title,
            self.menu_bar,
            submenu_function,
        )
        self.addAction(sub_menu.getAction())
        return sub_menu
