
from typing import Tuple
from PySide2 import QtWidgets, QtGui, QtCore

from csv_remapper.components import dialogs
from csv_remapper.constants import *

# noinspection PyUnreachableCode
if False:
    from csv_remapper.widgets.data_editor import DataEditor


class DragAndDropHeaderView(QtWidgets.QHeaderView):
    mime_type = 'application/x-qabstractitemmodeldatalist'
    data_dragged = QtCore.Signal(tuple)
    data_dropped = QtCore.Signal(tuple)

    def __init__(self, parent=None, mappable=False):  # type: (DataEditor, bool) -> None
        QtWidgets.QHeaderView.__init__(self, QtCore.Qt.Horizontal, parent)
        self.parent = parent
        self._parent_type = parent.type.split(MAPPING_SEPARATOR)[0]  # e.g.: Output/Some_Data -> Output
        self._data = None

        style = QtWidgets.QStyleFactory.create('Fusion')  # required for header colour changes
        self.setStyle(style)

        self.setDragEnabled(mappable)
        self.setAcceptDrops(mappable)
        self.setSectionsClickable(True)

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self._data = self.build_mime_data(event)

    def mouseMoveEvent(self, event):  # type: (QtGui.QMouseEvent) -> None
        if event.buttons() & QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            drag.setMimeData(self.encode_mime_data(self._data))
            drag.exec_(QtCore.Qt.MoveAction)

    def dragEnterEvent(self, event):
        if isinstance(event.source(), type(self)) and event.source() is not self:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.source() is not self:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        source = event.source()  # type: DragAndDropHeaderView
        source_data = tuple(self.decode_mime_mata(event.mimeData()))
        target_data = self.build_mime_data(event)
        # disallow mapping of Alias Value columns between Output tables
        if source.parent_type == self.parent_type and ALIAS_FIELD_NAME in (source_data[-1], target_data[-1]):
            dialogs.validation_message(
                'Invalid Mapping', f'{ALIAS_FIELD_NAME} column mapping between {OUTPUT_K} templates is not allowed',
                buttons=False
            )
            return
        if target_data[0] == INPUT_K and target_data[-1] != ALIAS_FIELD_NAME:
            first = target_data
            last = source_data
        elif source_data[0] == OUTPUT_K and MAPPING_SEPARATOR in target_data[0]:
            first = target_data
            last = source_data
        else:
            first = source_data
            last = target_data
        self.data_dropped.emit((first, last))

    def encode_mime_data(self, items):
        data = QtCore.QByteArray()
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream.writeQStringList(items)
        mimedata = QtCore.QMimeData()
        mimedata.setData(self.mime_type, data)
        return mimedata

    def decode_mime_mata(self, mimedata):
        stream = QtCore.QDataStream(mimedata.data(self.mime_type))
        data = stream.readQStringList()
        return data

    def build_mime_data(self, event):  # type: (QtCore.QEvent) -> Tuple[str, str, str, str]
        column = self.logicalIndexAt(event.pos())
        column_name = self.model().headerData(column, QtCore.Qt.Horizontal)
        data = (self.parent.type, self.parent.name, str(column), column_name)
        return data

    @property
    def parent_type(self):
        return self._parent_type
