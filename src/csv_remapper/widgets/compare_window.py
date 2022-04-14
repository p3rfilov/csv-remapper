
from PySide2 import QtWidgets, QtGui, QtCore

from csv_remapper.constants import *

# noinspection PyUnreachableCode
if False:
    from csv_remapper.widgets.data_editor import DataEditor


class CompareWindow(QtWidgets.QWidget):
    def __init__(self, name, left_widget, right_widget, parent=None):
        # type: (str, DataEditor, DataEditor, QtCore.QObject) -> None
        super(CompareWindow, self).__init__(parent)
        self.name = name
        self.left_widget = left_widget
        self.right_widget = right_widget
        self.setWindowTitle(name)
        self.setWindowIcon(QtGui.QIcon(APP_ICON))

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.left_widget)
        self.layout().addWidget(self.right_widget)

        self.showMaximized()
        self.left_widget.show()
        self.right_widget.show()
