
from PySide2 import QtWidgets, QtGui, QtCore

from csv_remapper.resources import data_editor_ui
from csv_remapper.components import (
    models,
    views,
    dialogs,
    io_handlers,
    datatypes,
    decorators,
)
from csv_remapper.constants import *


class DataEditor(QtWidgets.QWidget):
    lookup_mode_changed = QtCore.Signal(str)

    @decorators.exception
    def __init__(self, name, template_type, dir_handler, parent=None, editable=True, mappable=False, hide_data=False,
                 alias_settings=True, alias_data=True):
        # type: (str, str, io_handlers.AppDirectoryHandler, QtCore.QObject, bool, bool, bool, bool, bool) -> None
        super(DataEditor, self).__init__(parent)
        self.dir_handler = dir_handler
        self.csv_handler = io_handlers.CsvFileHandler()
        self._name = name
        self._type = template_type
        self._editable = editable
        self._mappable = mappable
        self._hide_data = hide_data
        self._alias_settings = alias_settings
        self._alias_data = alias_data

        self.ui = data_editor_ui.Ui_DataEditor()
        self.ui.setupUi(self)
        self.setWindowTitle(name)
        self.setWindowIcon(QtGui.QIcon(APP_ICON))
        self.ui.grp_name.setTitle(name)

        self.model = models.CsvDataModel(
            self, dir_handler=dir_handler, editable=self._editable, hide_data=self._hide_data
        )
        self.ui.tbl_data.setModel(self.model)
        self.header = views.DragAndDropHeaderView(self, mappable=self._mappable)
        self.ui.tbl_data.setHorizontalHeader(self.header)

        self.ui.tbl_data.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.lab_tooltip.setText(ALIAS_TOOLTIP_TEXT)

        self.setup_widgets()
        self._connect_signals()

    def _connect_signals(self):
        self.ui.tbl_data.customContextMenuRequested.connect(self.display_context_menu)
        self.model.data_loaded.connect(self.on_data_loaded)
        self.model.data_changed.connect(self.resize_columns_to_contents)
        self.ui.btn_update.pressed.connect(self.update_from_csv)
        self.ui.btn_export.pressed.connect(self.export_as_csv)
        self.ui.btn_save.pressed.connect(self.save_data)
        self.ui.btn_copy_column.pressed.connect(self.copy_values_to_alias_column)
        self.ui.cbx_lookup_mode.activated.connect(self._set_tooltip)
        self.ui.cbx_lookup_mode.currentIndexChanged.connect(
            lambda: self.lookup_mode_changed.emit(self.ui.cbx_lookup_mode.currentText())
        )

    def closeEvent(self, event):
        self.about_to_close()
        event.accept()

    def about_to_close(self):
        if self.model.data_has_changed and self.model.file and os.path.isfile(self.model.file):
            result = dialogs.validation_message(
                'Data has changed', f'The data in "{self.name}" has changed. Would you like to save the changes?'
            )
            if result:
                self.model.save_data()
            else:
                self.model.reset_changed_flag()

    @decorators.exception
    def display_context_menu(self, *args, **kwargs):
        if self._editable:
            menu = dialogs.ContextMenu(
                self, actions=(
                    'New Row',
                    'New Column',
                    '_',
                    'Move Row Up',
                    'Move Row Down',
                    'Move Column Right',
                    'Move Column Left',
                    '_',
                    'Remove Row',
                    'Remove Column'
                )
            )
            index = self.ui.tbl_data.currentIndex()
            if menu.action == 'New Row':
                self.model.insertRow(index.row())
                self.resize_columns_to_contents()
            elif menu.action == 'New Column':
                result = dialogs.InputDialog(
                    mode=datatypes.InputMode.COLUMN_NAME,
                    handler=self.dir_handler,
                    model=self.model,
                )
                text = result.textValue()
                self.model.insertColumn(index.column(), text)
                self.resize_columns_to_contents()
            elif menu.action == 'Move Row Up':
                self.model.move_row(index.row(), 1)
            elif menu.action == 'Move Row Down':
                self.model.move_row(index.row(), -1)
            elif menu.action == 'Move Column Right':
                self.model.move_column(index.column(), -1)
            elif menu.action == 'Move Column Left':
                self.model.move_column(index.column(), 1)
            elif menu.action == 'Remove Row':
                if index.row() >= 0:
                    result = dialogs.validation_message('Sure?', 'Delete selected Row?')
                    if result:
                        self.model.removeRow(index.row())
                        self.resize_columns_to_contents()
            elif menu.action == 'Remove Column':
                result = dialogs.validation_message('Sure?', 'Delete selected Column?')
                if result:
                    self.model.removeColumn(index.column())
                    self.resize_columns_to_contents()

    @decorators.exception
    def update_from_csv(self):
        new_file = dialogs.get_files_dialog(single_file=True)[0]
        if new_file and self.model.the_data:
            primary_key = dialogs.InputDialog(
                title='Primary key Column',
                mode=datatypes.InputMode.TABLE_COLUMN,
                model=self.model,
                handler=self.dir_handler
            ).textValue()
            if primary_key:
                new_data = self.csv_handler.read(new_file)[DATA_K]
                if new_data:
                    self.model.update_data(new_data, primary_key)

    @decorators.exception
    def export_as_csv(self):
        file_path = dialogs.save_file_dialog()
        if file_path:
            self.model.save_data(file_path)

    @decorators.exception
    def save_data(self):
        if not self.model.file:
            self.export_as_csv()
        else:
            self.model.save_data()

    @decorators.exception
    def copy_values_to_alias_column(self):
        name = dialogs.InputDialog(
            title='Copy Values',
            label=f'Copy Values to "{ALIAS_FIELD_NAME}" from this Column:',
            mode=datatypes.InputMode.TABLE_COLUMN,
            model=self.model,
            handler=self.dir_handler
        ).textValue()
        self.model.copy_values(name, ALIAS_FIELD_NAME)

    def on_data_loaded(self):
        self.resize_columns_to_contents()
        self._toggle_data_visibility()

    def resize_columns_to_contents(self):
        self.ui.tbl_data.resizeColumnsToContents()
        self.ui.tbl_data.horizontalHeader().setStretchLastSection(True)

    def setup_widgets(self):
        self.ui.cbx_lookup_mode.clear()
        self.ui.cbx_lookup_mode.addItems(datatypes.LookupModes.all())

        screen_height = QtGui.QGuiApplication.primaryScreen().availableGeometry().height() * DATA_EDITOR_HEADER_ONLY_HEIGHT

        if not self._editable:
            self.ui.lab_tooltip.hide()
            self.ui.grp_data_editor.setEnabled(False)
            self.ui.grp_data_editor.hide()
        if self._mappable:
            self.ui.tbl_data.horizontalHeader().setMinimumHeight(screen_height)
        if self._hide_data:
            self.ui.tbl_data.setMaximumHeight(screen_height + 2)
            self.ui.tbl_data.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        if not self._alias_settings:
            self.ui.grp_alias_settings.setEnabled(False)
            self.ui.grp_alias_settings.hide()
        if not self._alias_data:
            self.ui.grp_alias_data.setEnabled(False)
            self.ui.grp_alias_data.hide()

    def set_combo_index_by_name(self, name):
        index = self.ui.cbx_lookup_mode.findData(name, QtCore.Qt.DisplayRole)
        if index != -1:
            self.ui.cbx_lookup_mode.setCurrentIndex(index)
            self._set_tooltip()

    def _set_tooltip(self):
        name = self.ui.cbx_lookup_mode.currentText()
        if name == datatypes.LookupModes.REGEX:
            self.ui.lab_tooltip.setText(ALIAS_REGEX_TOOLTIP_TEXT)
        else:
            self.ui.lab_tooltip.setText(ALIAS_TOOLTIP_TEXT)

    def _toggle_data_visibility(self):
        self.ui.tbl_data.clearSelection()
        for row in range(self.ui.tbl_data.model().rowCount()):
            self.ui.tbl_data.setRowHidden(row, self._hide_data)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def view(self):
        return self.ui.tbl_data

    @property
    def data_hidden(self):
        return self._hide_data

    @property
    def lookup_mode(self):
        return self.ui.cbx_lookup_mode.currentText()


if __name__ == '__main__':
    import sys
    import os
    from PySide2 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)

    handler = io_handlers.AppDirectoryHandler()
    dialog1 = DataEditor('Template1', INPUT_K, dir_handler=handler)
    dialog2 = DataEditor('Template2', OUTPUT_K, dir_handler=handler)
    dialog1.show()
    dialog2.show()

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    test_file = os.path.join(root_dir, 'tests', 'CSV Data', 'Netsuite Standard Format Upload.csv')

    dialog1.model.load_data(test_file, add_alias_column=True)
    dialog2.model.load_data(test_file)

    sys.exit(app.exec_())
