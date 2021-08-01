"""
Example of how to use the "Treeview" class
"""

import sys
from PyQt5 import QtWidgets
from window import Window
from treeview import Treeview

# Creates the application
app = QtWidgets.QApplication(sys.argv)

# Creates the data viewer window
window = Window('Testing Data Viewer Table')

# Creates the data viewer table
treeview = Treeview(window, ('Col0', 'Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7'))

# Creates 3 parent lines
parent_line_item_0 = treeview.insertParentLineItem('testing_0')
parent_line_item_1 = treeview.insertParentLineItem('testing_1')
parent_line_item_2 = treeview.insertParentLineItem('testing_2')

# Inserts data in the "parent_line_item_0"
treeview.insertChildrenLineData(parent_line_item_0, ['00', '01', '02', '03', '04', '05', '06', '07'])
treeview.insertChildrenLineData(parent_line_item_0, ['00', '01', '02', '03', '04', '05', '06', '07'])
treeview.insertChildrenLineData(parent_line_item_0, ['00', '01', '02', '03', '04', '05', '06', '07'])

# Inserts data in the "parent_line_item_1"
treeview.insertChildrenLineData(parent_line_item_1, ['10', '11', '12', '13', '14', '15', '16', '17'])
treeview.insertChildrenLineData(parent_line_item_1, ['10', '11', '12', '13', '14', '15', '16', '17'])
treeview.insertChildrenLineData(parent_line_item_1, ['10', '11', '12', '13', '14', '15', '16', '17'])

# Inserts data in the "parent_line_item_2"
treeview.insertChildrenLineData(parent_line_item_2, ['20', '21', '22', '23', '24', '25', '26', '27'])
treeview.insertChildrenLineData(parent_line_item_2, ['20', '21', '22', '23', '24', '25', '26', '27'])
treeview.insertChildrenLineData(parent_line_item_2, ['20', '21', '22', '23', '24', '25', '26', '27'])

# Expand the parent lines
treeview.expandParentLines()
treeview.resizeColumnsToTreeViewWidth()

# Shows the data viewer window
window.showMaximized()

# Ends the application when everything is closed
sys.exit(app.exec_())
