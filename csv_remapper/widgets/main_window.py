
from PySide2 import QtWidgets, QtGui, QtCore

import csv_remapper
from csv_remapper.resources import main_window_ui
from csv_remapper.components import (
    io_handlers,
    dialogs,
    decorators,
    wizards,
    remappers,
)
from csv_remapper.widgets import (
    template_editor,
    data_editor,
    compare_window,
)
from csv_remapper.constants import *


class MainWindow(QtWidgets.QMainWindow):
    @decorators.exception
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dir_handler = io_handlers.AppDirectoryHandler()
        self.csv_handler = io_handlers.CsvFileHandler()
        self.json_handler = io_handlers.JsonFileHandler()
        self.template_creator = wizards.TemplateCreator(self.dir_handler)
        self._template_editor = None
        self._root_watcher = None
        self._compare_window = None
        self._drop_label = None

        self.ui = main_window_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME + ' - ' + csv_remapper.__version__)
        self.setWindowIcon(QtGui.QIcon(APP_ICON))

        self.show()  # delay until widgets are loaded for correct drop_label positioning

        self._display_drop_label()
        self._init_app_settings()
        self._connect_signals()

        self.ui.action_options.setEnabled(False)

    @decorators.exception
    def resizeEvent(self, event):
        self._display_drop_label()
        super(MainWindow, self).resizeEvent(event)

    def _init_app_settings(self, new_location=False):
        if not self.dir_handler.root or new_location:
            location = dialogs.get_directory_dialog(title='Please select Template Storage location')
            if location.strip():
                self.dir_handler = io_handlers.AppDirectoryHandler(location)
                self.dir_handler.write_settings(TEMPLATE_ROOT_DIR_K, location)
                self.template_creator = wizards.TemplateCreator(self.dir_handler)
            elif not new_location and not location.strip():
                self.close()
                self.deleteLater()
                return
        if not self.dir_handler.get_existing_template_names()[OUTPUT_K]:
            self.ui.action_new_input.setEnabled(False)
        else:
            self.ui.action_new_input.setEnabled(True)
        self._setup_root_watcher()
        self._populate_template_combo()

    def _setup_root_watcher(self):
        self._root_watcher = QtCore.QFileSystemWatcher()
        if self.dir_handler.root:
            paths = [os.path.join(self.dir_handler.root, t) for t in TEMPLATE_TYPES]
            self._root_watcher.addPaths(paths)
            self._root_watcher.directoryChanged.connect(lambda: self._init_app_settings())

    def _populate_template_combo(self):
        self.ui.cbx_template.clear()
        all_templates = self.dir_handler.get_existing_template_names()
        for name in all_templates[OUTPUT_K]:
            self.ui.cbx_template.addItem(name)

    def _connect_signals(self):
        self.ui.action_new_input.triggered.connect(self.create_input_template)
        self.ui.action_new_output.triggered.connect(self.create_output_template)
        self.ui.action_edit_templates.triggered.connect(self.edit_templates)
        self.ui.action_change_directory.triggered.connect(lambda: self._init_app_settings(new_location=True))
        self.ui.tbl_items.item_double_clicked.connect(self.view_file)
        self.ui.tbl_items.items_dropped.connect(self._display_drop_label)
        self.ui.btn_browse.clicked.connect(self.browse_files)
        self.ui.btn_remove.clicked.connect(self.remove_selected_files)
        self.ui.btn_preview.clicked.connect(self.preview_selected_item)
        self.ui.btn_remap.clicked.connect(self.remap_files)

    def create_output_template(self):
        new_template = self.template_creator.create_output_template()
        if new_template:
            self._init_app_settings()

    def create_input_template(self):
        self.template_creator.create_input_template()

    def edit_templates(self):
        self._template_editor = template_editor.TemplateEditor('Template Editor', self.dir_handler)
        self._template_editor.setWindowModality(QtCore.Qt.WindowModal)
        self._template_editor.showMaximized()

    def browse_files(self):
        csv_files = dialogs.get_files_dialog()
        if csv_files:
            self.ui.tbl_items.add_files(csv_files)
            self._display_drop_label()

    def remove_selected_files(self):
        self.ui.tbl_items.remove_files()
        self._display_drop_label()

    @decorators.exception
    def view_file(self, file_path):
        editor = data_editor.DataEditor(
            file_path,
            'Edit',
            dir_handler=self.dir_handler,
            alias_settings=False,
            alias_data=False
        )
        editor.model.load_data(file_path)
        editor.setWindowModality(QtCore.Qt.WindowModal)
        editor.show()

    @decorators.exception
    def remap_files(self, out_dir=None):  # type: (str) -> None
        if self.ui.tbl_items.rowCount() > 0:
            out_template = self._get_output_template_name()
            out_dir = out_dir or dialogs.get_directory_dialog(title='Select Output Directory...')
            if not out_template or not out_dir:
                return
            for i in range(self.ui.tbl_items.rowCount()):
                csv_file = self.ui.tbl_items.item(i, 0).text()
                remapped_data = remappers.remap_csv_file(csv_file, out_template, self.dir_handler)
                io_handlers.write_remapped_data(csv_file, out_dir, remapped_data)
            dialogs.validation_message('Done', 'All files have been remapped', buttons=False)

    @decorators.exception
    def preview_selected_item(self):
        csv_file = self.ui.tbl_items.currentItem().text() if self.ui.tbl_items.currentItem() else ''
        out_template = self._get_output_template_name()
        if csv_file and out_template:
            remapped_data = remappers.remap_csv_file(csv_file, out_template, self.dir_handler)
            if remapped_data:
                input_editor = data_editor.DataEditor(
                    '[ Original ]',
                    'Edit',
                    dir_handler=self.dir_handler,
                    alias_settings=False,
                    alias_data=False,
                    editable=False
                )
                input_editor.model.load_data(csv_file)
                input_editor.setWindowModality(QtCore.Qt.WindowModal)

                output_editor = data_editor.DataEditor(
                    '[ Remapped Data ]',
                    'Edit',
                    dir_handler=self.dir_handler,
                    alias_settings=False,
                    alias_data=False
                )
                output_editor.model.set_data(remapped_data)
                output_editor.setWindowModality(QtCore.Qt.WindowModal)

                self._compare_window = compare_window.CompareWindow(csv_file, input_editor, output_editor)

    def _get_output_template_name(self):
        out_template = self.ui.cbx_template.currentText()
        if not out_template:
            dialogs.validation_message('Error', 'Output Template is undefined', buttons=False)
        return out_template

    @decorators.exception
    def _display_drop_label(self):
        if self.ui.tbl_items.rowCount() < 1:
            if not self._drop_label:
                self._drop_label = QtWidgets.QLabel(self.ui.tbl_items)
                self._drop_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
                self._drop_label.setAlignment(QtCore.Qt.AlignCenter)
                self._drop_label.setText('Drop CSV files here')
                self._drop_label.setStyleSheet('font-weight: bold;')
            if not self._drop_label.isVisible():
                self._drop_label.show()
            self._drop_label.resize(self.ui.tbl_items.size())
        elif self._drop_label and self._drop_label.isVisible():
            self._drop_label.hide()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
