
from typing import List
from PySide2 import QtWidgets, QtCore

from csv_remapper.constants import *


class DragDropTable(QtWidgets.QTableWidget):
    items_dropped = QtCore.Signal()
    item_double_clicked = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(DragDropTable, self).__init__(parent)
        self.setAcceptDrops(True)
        self._connect_signals()

    def _connect_signals(self):
        self.cellDoubleClicked.connect(self.emit_file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        files = [u.toLocalFile() for u in urls if u.toLocalFile().lower().endswith(TEMPLATE_FORMAT)]
        self.add_files(files)
        self.items_dropped.emit()

    def emit_file_path(self, row, column):  # type: (int, int) -> None
        if row >= 0:
            file_path = self.item(row, 0).text()
            self.item_double_clicked.emit(file_path)

    def add_files(self, files):  # type: (List[str]) -> None
        for f in files:
            if not self._file_already_added(f):
                self.insertRow(0)
                item = QtWidgets.QTableWidgetItem(f)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.setItem(0, 0, item)

    def remove_files(self):
        selection = self.selectedIndexes()
        for index in reversed(selection):
            self.removeRow(index.row())

    def _file_already_added(self, file_path):  # type: (str) -> bool
        all_files = []
        for row in range(self.rowCount()):
            all_files.append(self.item(row, 0).text())
        if file_path in all_files:
            return True
        return False
