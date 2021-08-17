from PyQt5 import QtWidgets


class WidgetInterface(QtWidgets.QWidget):
    def __init__(self, CentralWidget):
        super().__init__(CentralWidget)
        self.__width = 0
        self.__height = 0

    def incrementInternalWidth(self, width):
        self.__width += width

    def getInternalWidth(self):
        return self.__width

    def incrementInternalHeight(self, height):
        self.__height += height

    def getInternalHeight(self):
        return self.__height
