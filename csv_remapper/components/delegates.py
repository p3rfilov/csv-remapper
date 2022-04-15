
from typing import Tuple
from PySide2 import QtWidgets, QtCore


class ComboBoxDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent, options):  # type: (QtCore.QObject, Tuple[str]) -> None
        self._options = options
        super(ComboBoxDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(self._options)
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setCurrentIndex(editor.findText(value))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), QtCore.Qt.EditRole)
