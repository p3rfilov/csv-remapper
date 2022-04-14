
from PySide2 import QtWidgets, QtCore, QtGui

from csv_remapper.components import (
    io_handlers,
    dialogs,
)
from csv_remapper.constants import *


class CsvDataModel(QtCore.QAbstractTableModel):
    data_changed = QtCore.Signal()
    data_loaded = QtCore.Signal()

    def __init__(self, parent, dir_handler, editable=True, hide_data=False):
        super(CsvDataModel, self).__init__(parent)
        self.dir_handler = dir_handler
        self.csv_handler = io_handlers.CsvFileHandler()
        self.parent = parent
        self._editable = editable
        self._hide_data = hide_data  # hide data as well, to correctly resize columns to header text
        self._columns = []
        self._data = []
        self._file = None
        self._mapping_model = None
        self._changed = False

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._columns)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if self._hide_data:
            return None
        if not index.isValid():
            return None
        if not all([self._columns, self._data]):
            return None
        value = self._data[index.row()][self._columns[index.column()]]
        if role in (QtCore.Qt.EditRole, QtCore.Qt.DisplayRole):
            return str(value) if value else value
        return None

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        elif self._editable:
            return QtCore.Qt.ItemFlags(QtCore.QAbstractTableModel.flags(self, index) | QtCore.Qt.ItemIsEditable)
        else:
            return QtCore.Qt.ItemFlags(QtCore.QAbstractTableModel.flags(self, index))

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        column_name = self._columns[index.column()]
        current_data = self._data[index.row()]
        if not self._data[index.row()][column_name] == value:
            if column_name == ALIAS_FIELD_NAME and self.is_alias_already_in_use(value, current_data):
                dialogs.validation_message(
                    'Name Not Unique', 'This Alias already exists. Try providing a longer, more specific Alias.   ',
                    buttons=False
                )
                return False
            self._data[index.row()][column_name] = value
            self._data_changed_event()
        return self._data[index.row()][column_name] == value

    def headerData(self, col, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and col in range(len(self._columns)):
            if role == QtCore.Qt.DisplayRole:
                return self._columns[col]
            elif role == QtCore.Qt.BackgroundRole and self.is_column_mapped(col):
                if self._mapping_model and self._mapping_model.view:
                    row = self._mapping_model.view.currentIndex().row()
                    if row != -1 and row in range(len(self._mapping_model.the_data[MAPPINGS_K])):
                        column_name = self._columns[col]
                        editor_name = self.parent.name
                        mapping_data = self._mapping_model.the_data[MAPPINGS_K][row]
                        mapping_name = mapping_data[NAME_K].split(MAPPING_SEPARATOR)[-1]
                        source_name = self._mapping_model.the_data.get(SOURCE_K, '').split(MAPPING_SEPARATOR)[-1]
                        if len({column_name, editor_name} & {mapping_name, source_name, mapping_data[SOURCE_COLUMN_K],
                                                             mapping_data[TARGET_COLUMN_K]}) == 2:
                            return QtGui.QBrush(QtGui.QColor(*COLOURS['blue']), QtCore.Qt.SolidPattern)
                return QtGui.QBrush(QtGui.QColor(*COLOURS['green']))
        return None

    def insertColumn(self, column, name, parent=QtCore.QModelIndex()):
        if name and name not in self._columns:
            self.layoutAboutToBeChanged.emit()
            if column < 0:
                column = len(self._columns)
            self._columns.insert(column, name)
            for row in self._data:
                row[name] = ''
            self._data_changed_event()
            self.layoutChanged.emit()
            return True
        return False

    def removeColumn(self, column, parent=QtCore.QModelIndex()):
        self.layoutAboutToBeChanged.emit()
        column_name = self._columns[column]
        for row in self._data:
            row.pop(column_name, None)
        self._columns.pop(column)
        self._data_changed_event()
        self.layoutChanged.emit()
        return True

    def insertRow(self, row):
        self.layoutAboutToBeChanged.emit()
        self._data.insert(row, {k: '' for k in self._columns})
        self._data_changed_event()
        self.layoutChanged.emit()
        return True

    def removeRow(self, row):
        self.layoutAboutToBeChanged.emit()
        self._data.pop(row)
        self._data_changed_event()
        self.layoutChanged.emit()
        return True

    def set_file(self, file_path):  # type: (str) -> None
        self._file = file_path

    def set_mapping_model(self, model):  # type: (MappingDataModel) -> None
        self._mapping_model = model

    def is_column_mapped(self, col):  # type: (int) -> bool
        if self._mapping_model:
            data = self._mapping_model.the_data
            editor_name = self.parent.name
            source_names = data.get(SOURCE_K, '').split(MAPPING_SEPARATOR)
            source_columns = [c[SOURCE_COLUMN_K] for c in data.get(MAPPINGS_K, [])]
            if (editor_name in source_names) and (self._columns[col] in source_columns):
                return True
            for mapping in data.get(MAPPINGS_K, []):
                target_names = mapping[NAME_K].split(MAPPING_SEPARATOR)
                target_columns = mapping[TARGET_COLUMN_K]
                if (editor_name in target_names) and (self._columns[col] in target_columns):
                    return True
        return False

    def is_alias_already_in_use(self, value, current_data):  # type: (str, dict) -> bool
        if value:
            split_values = [s.lower() for s in value.split(ALIAS_DATA_SEPARATOR) if s]
            for data in self._data:
                existing_values = [s.lower() for s in data[ALIAS_FIELD_NAME].split(ALIAS_DATA_SEPARATOR) if s]
                if data != current_data and len(set(split_values) & set(existing_values)) == 1:
                    return True
        return False

    def reset_changed_flag(self):
        self._changed = False

    def load_data(self, the_file=None, add_alias_column=False):  # type: (str, bool) -> None
        if the_file:
            self._file = the_file
        else:
            the_file = self._file

        self.layoutAboutToBeChanged.emit()
        all_data = self.csv_handler.read(the_file)
        self._columns = all_data[HEADERS_K]
        self._data = all_data[DATA_K]
        if add_alias_column:
            self.add_alias_column()
        self.layoutChanged.emit()
        self.data_loaded.emit()

    def save_data(self, the_file=None):  # type: (str) -> None
        if not the_file:
            the_file = self._file
        if the_file:
            all_data = {HEADERS_K: self._columns, DATA_K: self._data}
            self.csv_handler.write(the_file, all_data)
            self._changed = False

    def set_data(self, data):  # type: (dict) -> None
        self.layoutAboutToBeChanged.emit()
        self._columns = data[HEADERS_K]
        self._data = data[DATA_K]
        self.layoutChanged.emit()
        self.data_loaded.emit()

    def update_data(self, new_data, primary_key):  # type: (list, str) -> None
        if primary_key != NONE_STRING and primary_key not in new_data[0]:
            dialogs.validation_message(
                'Error', f'Column "{primary_key}" does not exist in the incoming file!', buttons=False
            )
            return

        if primary_key == NONE_STRING:
            result = dialogs.validation_message(
                'Replace data by Row order?',
                'No primary key column was provided. The data will be replaced by row order.'
            )
            if not result:
                return

        self.layoutAboutToBeChanged.emit()
        for column in new_data[0].keys():
            if column not in self._columns:
                self.insertColumn(self.columnCount() - 1, column)
        if primary_key == NONE_STRING:
            # if no primary key column was provided, replace data by row order
            extra_rows = len(new_data) - len(self._data)
            if extra_rows > 0:
                for row in range(extra_rows):
                    self.insertRow(self.rowCount())
            for row in range(len(new_data)):
                self._data[row].update(new_data[row])
        else:
            # replace data by matching row primary key values
            new_rows = []
            for row in range(len(new_data)):
                match = False
                key_value = new_data[row][primary_key]
                for r in range(len(self._data)):
                    if key_value == self._data[r][primary_key]:
                        self._data[r].update(new_data[row])
                        match = True
                        break
                if not match:
                    new_rows.append(new_data[row])
            for row_data in new_rows:
                self.insertRow(self.rowCount())
                self._data[self.rowCount() - 1].update(row_data)
        self.layoutChanged.emit()
        self._data_changed_event()

    def add_alias_column(self):
        self.insertColumn(len(self._columns), ALIAS_FIELD_NAME)
        self._changed = False

    def move_row(self, row, offset):  # type: (int, int) -> None
        new_index = row - offset
        if row != -1 and new_index in range(len(self._data)):
            self.layoutAboutToBeChanged.emit()
            self._data.insert(new_index, self._data.pop(row))
            self._data_changed_event()
            self.layoutChanged.emit()

    def move_column(self, column, offset):  # type: (int, int) -> None
        new_index = column - offset
        if column != -1 and new_index in range(len(self._columns)):
            self.layoutAboutToBeChanged.emit()
            self._columns.insert(new_index, self._columns.pop(column))
            self._data_changed_event()
            self.layoutChanged.emit()

    def copy_values(self, source_column, target_column):  # type: (str, str) -> bool
        if source_column not in self.columns or target_column not in self.columns:
            dialogs.validation_message(
                'Error', f'Invalid column Names supplied: {source_column, target_column}', buttons=False
            )
            return False
        result = dialogs.validation_message(
            'Warning', f'This will override all values in the "{target_column}" column. Continue?'
        )
        if result:
            self.layoutAboutToBeChanged.emit()
            for data in self._data:
                data[target_column] = data[source_column]
            self._data_changed_event()
            self.layoutChanged.emit()
            return True
        return False

    def _data_changed_event(self):
        self._changed = True
        self.data_changed.emit()

    @property
    def data_has_changed(self):
        return self._changed

    @property
    def the_data(self):
        return self._data

    @property
    def file(self):  # type: () -> str
        return self._file

    @property
    def columns(self):
        return self._columns


class MappingDataModel(QtCore.QAbstractTableModel):
    data_changed = QtCore.Signal()
    data_loaded = QtCore.Signal()

    def __init__(self, parent=None):
        super(MappingDataModel, self).__init__(parent)
        self.handler = io_handlers.JsonFileHandler()
        self._file = None
        self._view = None
        self._columns = (NAME_K, SOURCE_COLUMN_K, TARGET_COLUMN_K, IN_DATA_K, OUT_DATA_K)
        self._data = {}
        self._changed = False
        self.data_column_width = 130

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._columns)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data.get(MAPPINGS_K, []))

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if not all([self._columns, self._data.get(MAPPINGS_K)]):
            return None
        value = self._data[MAPPINGS_K][index.row()][self._columns[index.column()]]
        if role in (QtCore.Qt.EditRole, QtCore.Qt.DisplayRole):
            column_name = self._columns[index.column()]
            if column_name == SOURCE_COLUMN_K:
                name = self._data.get(SOURCE_K, '').split(MAPPING_SEPARATOR)[-1]
                value = ' | '.join([name, value])
            elif column_name == TARGET_COLUMN_K:
                name = self._data[MAPPINGS_K][index.row()][NAME_K].split(MAPPING_SEPARATOR)[-1]
                value = ' | '.join([name, value])
            return str(value) if value else value
        return None

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        elif self._columns[index.column()] in (IN_DATA_K, OUT_DATA_K):
            return QtCore.Qt.ItemFlags(QtCore.QAbstractTableModel.flags(self, index) | QtCore.Qt.ItemIsEditable)
        else:
            return QtCore.Qt.ItemFlags(QtCore.QAbstractTableModel.flags(self, index))

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        column_name = self._columns[index.column()]
        if not self._data[MAPPINGS_K][index.row()][column_name] == value:
            self._data[MAPPINGS_K][index.row()][column_name] = value
            self._data_changed_event()
        return self._data[MAPPINGS_K][index.row()][column_name] == value

    def headerData(self, col, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if not col < 0 and col < len(self._columns):
                return self._columns[col]
        return None

    def set_file(self, file_path):  # type: (str) -> None
        self._file = file_path

    def set_view(self, view_widget):  # type: (QtWidgets.QTableView) -> None
        self._view = view_widget

    def load_data(self, the_file=None):  # type: (str) -> None
        if the_file:
            self._file = the_file
        else:
            the_file = self._file

        self.layoutAboutToBeChanged.emit()
        self._data = self.handler.read(the_file)
        self._changed = False
        self.layoutChanged.emit()
        self.data_loaded.emit()

    def save_data(self, the_file=None):  # type: (str) -> None
        if not the_file:
            the_file = self._file
        self.handler.write(the_file, self._data)
        self._changed = False

    def change_lookup_mode(self, new_mode):  # type: (str) -> None
        old_mode = self._data.get(LOOKUP_MODE_K)
        if old_mode and old_mode != new_mode:
            self._data[LOOKUP_MODE_K] = new_mode
            self._data_changed_event()

    def add_mapping(self, data, row=None):  # type: (dict, int) -> bool
        if not self.mapping_exists(data):
            self.layoutAboutToBeChanged.emit()
            if not row:
                row = self.rowCount()
            self._data[MAPPINGS_K].insert(row, data)
            self._data_changed_event()
            self.layoutChanged.emit()
            return True
        return False

    def move_row(self, row, offset):  # type: (int, int) -> None
        new_index = row - offset
        if row != -1 and new_index in range(len(self._data[MAPPINGS_K])):
            self.layoutAboutToBeChanged.emit()
            self._data[MAPPINGS_K].insert(new_index, self._data[MAPPINGS_K].pop(row))
            self._data_changed_event()
            self.layoutChanged.emit()

    def delete_row(self, row):  # type: (int) -> None
        if row != -1:
            self.layoutAboutToBeChanged.emit()
            self._data[MAPPINGS_K].pop(row)
            self._data_changed_event()
            self.layoutChanged.emit()

    def mapping_exists(self, data):  # type: (dict) -> bool
        current_mappings = []
        for mapping in self._data[MAPPINGS_K]:
            _data = {k: v for k, v in mapping.items() if k not in (IN_DATA_K, OUT_DATA_K)}
            current_mappings.append(_data)
        condensed_data = {k: v for k, v in data.items() if k not in (IN_DATA_K, OUT_DATA_K)}
        if condensed_data in current_mappings:
            return True
        return False

    def _data_changed_event(self):
        self._changed = True
        self.data_changed.emit()

    @property
    def data_has_changed(self):
        return self._changed

    @property
    def the_data(self):
        return self._data

    @property
    def columns(self):
        return self._columns

    @property
    def view(self):
        return self._view


class DirectoryListerModel(QtWidgets.QFileSystemModel):
    def __init__(self, root_dir, parent=None):  # type: (str, QtCore.QObject) -> None
        super(DirectoryListerModel, self).__init__(parent)
        self.setRootPath(root_dir)
        self.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)
        self.setReadOnly(True)
