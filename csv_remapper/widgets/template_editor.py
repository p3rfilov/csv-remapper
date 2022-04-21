
import shutil
from PySide2 import QtWidgets, QtGui, QtCore

from csv_remapper.resources import template_editor_ui
from csv_remapper.components import (
    models,
    delegates,
    dialogs,
    wizards,
    datatypes,
)
from csv_remapper.widgets import data_editor
from csv_remapper.constants import *

# noinspection PyUnreachableCode
if False:
    from typing import Tuple
    from csv_remapper.components.views import DragAndDropHeaderView
    from csv_remapper.components.io_handlers import AppDirectoryHandler


class TemplateEditor(QtWidgets.QWidget):
    def __init__(self, name, dir_handler, parent=None, templates=True, mappings=True, alias_data=True):
        # type: (str, AppDirectoryHandler, QtCore.QObject, bool, bool, bool) -> None
        super(TemplateEditor, self).__init__(parent)
        self.dir_handler = dir_handler
        self.template_creator = wizards.TemplateCreator(dir_handler)
        self._show_templates = templates
        self._show_mappings = mappings
        self._alias_data = alias_data
        self.input_template = None
        self.output_template = None

        self.ui = template_editor_ui.Ui_TemplateEditor()
        self.ui.setupUi(self)
        self.setWindowTitle(name)
        self.setWindowIcon(QtGui.QIcon(APP_ICON))

        self.directory_model = models.DirectoryListerModel(self.dir_handler.get_settings(TEMPLATE_ROOT_DIR_K))
        self.ui.tre_browse_templates.setModel(self.directory_model)

        self.mapping_model = models.MappingDataModel()
        self.mapping_model.set_view(self.ui.tbl_mappings)
        self.ui.tbl_mappings.setModel(self.mapping_model)
        self.ui.tbl_mappings.setItemDelegateForColumn(
            self.mapping_model.columns.index(IN_DATA_K),
            delegates.ComboBoxDelegate(self, datatypes.DataTypes.all())
        )
        self.ui.tbl_mappings.setItemDelegateForColumn(
            self.mapping_model.columns.index(OUT_DATA_K),
            delegates.ComboBoxDelegate(self, datatypes.DataTypes.all())
        )

        self._setup_template_browser()
        self._setup_mapping_editor()
        self._init_widgets()
        self._connect_signals()

    def closeEvent(self, event):
        # ensure user gets prompted if data has changed prior to closing
        self.clear_all_views()
        event.accept()

    def _connect_signals(self):
        self.ui.tbl_mappings.customContextMenuRequested.connect(self.display_mapping_context_menu)
        self.ui.btn_save.clicked.connect(self.save_all_changes)
        self.ui.tab_aliases.currentChanged.connect(self.on_alias_tab_changed)
        self.ui.btn_new_alias.clicked.connect(self.create_new_alias)
        self.ui.btn_new_alias_from_csv.clicked.connect(self.create_new_alias_from_csv)
        self.ui.btn_delete_template.clicked.connect(self.delete_selected_template)
        self.ui.btn_new_template.clicked.connect(self.on_new_template_clicked)
        temp_sel_model = self.ui.tre_browse_templates.selectionModel()
        temp_sel_model.currentRowChanged.connect(self.on_current_template_changed)
        map_sel_model = self.ui.tbl_mappings.selectionModel()
        map_sel_model.currentRowChanged.connect(self.on_current_mapping_selections_changed)

    def _init_widgets(self):
        self.ui.tab_aliases.clear()
        self.ui.grp_aliases.hide()
        self.ui.grp_mappings.hide()

    def _setup_template_browser(self):
        # resize widget depending on screen resolution
        width = QtGui.QGuiApplication.primaryScreen().availableGeometry().width() * TEMPLATE_BROWSER_WIDTH
        self.ui.grp_templates.setMaximumWidth(width)

        index = self.directory_model.index(self.directory_model.rootPath())
        self.ui.tre_browse_templates.setRootIndex(index)
        # hide all columns but the first one
        for i in range(self.ui.tre_browse_templates.model().columnCount())[1:]:
            self.ui.tre_browse_templates.hideColumn(i)

    def _setup_mapping_editor(self):
        self.ui.tbl_mappings.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tbl_mappings.horizontalHeader().setStretchLastSection(False)
        header = self.ui.tbl_mappings.horizontalHeader()
        header_data = self.mapping_model.columns
        for i in range(len(header_data)):
            if header_data[i] in (IN_DATA_K, OUT_DATA_K):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Fixed)
                self.ui.tbl_mappings.setColumnWidth(i, self.mapping_model.data_column_width)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def create_new_alias(self):
        if self.output_template:
            name = self.template_creator.create_alias_data(self.output_template.name)
            if name:
                self._setup_alias_widget_for_output_template(self.output_template.name, name)

    def create_new_alias_from_csv(self):
        if self.output_template:
            name = self.template_creator.create_alias_data_from_csv(self.output_template.name)
            if name:
                self._setup_alias_widget_for_output_template(self.output_template.name, name)

    def on_current_mapping_selections_changed(self):
        self.update_all_views()

    def on_current_template_changed(self, current_index, previous_index):
        names = []
        selection = current_index.data()
        all_templates = self.dir_handler.get_existing_template_names()
        for t in TEMPLATE_TYPES:
            names += all_templates[t]
        if selection in names and current_index != previous_index:
            self._change_template_view(selection, all_templates)
        self.on_alias_tab_changed(-1, selection)

    def _change_template_view(self, template_name, all_names):
        if template_name in all_names[INPUT_K]:
            self.clear_all_views()
            self.ui.grp_mappings.show()
            self.ui.grp_aliases.hide()
            self.setup_input_template_view(template_name)
        elif template_name in all_names[OUTPUT_K]:
            self.clear_all_views()
            self.ui.grp_mappings.show()
            self.ui.grp_aliases.show()
            self.setup_output_template_view(template_name)

    def setup_input_template_view(self, template_name):
        in_files = self.dir_handler.get_template_files(template_name, INPUT_K)
        self.mapping_model.load_data(in_files[MAPPINGS_K])
        output_temp_name = self.mapping_model.the_data.get(TARGET_K).split(MAPPING_SEPARATOR)[-1]
        out_files = self.dir_handler.get_template_files(output_temp_name, OUTPUT_K)
        alias_data_names = self.dir_handler.get_alias_data_names(output_temp_name)

        self.input_template = data_editor.DataEditor(
            template_name,
            INPUT_K,
            dir_handler=self.dir_handler,
            parent=self,
            mappable=True,
            alias_settings=False,
            alias_data=False
        )
        self.output_template = data_editor.DataEditor(
            output_temp_name,
            OUTPUT_K,
            dir_handler=self.dir_handler,
            parent=self,
            editable=False,
            mappable=True,
            hide_data=True,
            alias_settings=False,
            alias_data=True
        )
        for name in alias_data_names:
            self._setup_alias_widget_for_input_template(output_temp_name, name)

        self.input_template.model.load_data(in_files[FILE_K])
        self.input_template.model.set_mapping_model(self.mapping_model)
        self.output_template.model.load_data(out_files[FILE_K])
        self.output_template.model.set_mapping_model(self.mapping_model)
        self.ui.grp_template_veiws.layout().addWidget(self.input_template)
        self.ui.grp_template_veiws.layout().addWidget(self.output_template)
        self.input_template.header.data_dropped.connect(self.on_data_dropped)
        self.output_template.header.data_dropped.connect(self.on_data_dropped)
        self.input_template.show()
        self.output_template.show()

    def _setup_alias_widget_for_input_template(self, out_template_name, name):
        alias_widget = data_editor.DataEditor(
            name,
            f'Output/{out_template_name}',
            dir_handler=self.dir_handler,
            parent=self,
            editable=False,
            mappable=True,
            hide_data=True,
            alias_settings=False,
            alias_data=False
        )
        alias_widget.model.add_alias_column()
        alias_widget.model.set_mapping_model(self.mapping_model)
        alias_widget.header.data_dropped.connect(self.on_data_dropped)
        self.output_template.ui.grp_alias_data.layout().addWidget(alias_widget)
        alias_widget.show()

    def setup_output_template_view(self, template_name):
        out_files = self.dir_handler.get_template_files(template_name, OUTPUT_K)
        alias_value_names = self.dir_handler.get_alias_data_names(template_name)
        self.output_template = data_editor.DataEditor(
            template_name,
            OUTPUT_K,
            dir_handler=self.dir_handler,
            parent=self,
            mappable=True,
            alias_settings=False,
            alias_data=False
        )
        for name in alias_value_names:
            self._setup_alias_widget_for_output_template(template_name, name)
        if alias_value_names:
            self.on_alias_tab_changed(0)

        self.output_template.model.load_data(out_files[FILE_K])
        self.output_template.model.set_mapping_model(self.mapping_model)
        self.ui.grp_template_veiws.layout().addWidget(self.output_template)
        self.output_template.header.data_dropped.connect(self.on_data_dropped)
        self.output_template.show()

    def _setup_alias_widget_for_output_template(self, out_template_name, name):
        alias_data_files = self.dir_handler.get_alias_files(out_template_name, name)
        alias_widget = data_editor.DataEditor(
            name,
            f'Output/{out_template_name}',
            dir_handler=self.dir_handler,
            parent=self.ui.tab_aliases,
            editable=True,
            mappable=True,
            alias_settings=True,
            alias_data=False
        )
        alias_widget.model.load_data(alias_data_files[FILE_K], add_alias_column=True)
        alias_widget.model.save_data()  # save after adding Alias Data column
        self.mapping_model.load_data(alias_data_files[MAPPINGS_K])
        lookup_mode = self.mapping_model.the_data.get(LOOKUP_MODE_K, '')
        alias_widget.set_combo_index_by_name(lookup_mode)
        alias_widget.lookup_mode_changed.connect(self.mapping_model.change_lookup_mode)
        alias_widget.header.data_dropped.connect(self.on_data_dropped)
        alias_widget.model.set_mapping_model(self.mapping_model)

        self.ui.tab_aliases.addTab(alias_widget, name)

    def clear_all_views(self):
        self.save_mapping_changes()
        all_widgets = self.get_all_editor_widgets()
        for widget in all_widgets:
            widget.about_to_close()
        for widget in all_widgets:
            widget.close()
            widget.deleteLater()

    def update_all_views(self):
        all_widgets = self.get_all_editor_widgets()
        for widget in all_widgets:
            widget.model.layoutChanged.emit()
        self.mapping_model.layoutChanged.emit()

    def get_all_editor_widgets(self):
        template_widgets = self.ui.grp_template_veiws.findChildren(data_editor.DataEditor)
        alias_widgets = self.ui.tab_aliases.findChildren(data_editor.DataEditor)
        all_widgets = template_widgets + alias_widgets
        return all_widgets

    def save_mapping_changes(self):
        if self.mapping_model.data_has_changed:
            result = dialogs.validation_message(
                'Data has changed', 'The mapping data has changed. Would you like to save the changes?    '
            )
            if result:
                self.mapping_model.save_data()

    def on_data_dropped(self, data_tuple):
        if len(data_tuple) == 2:
            self.mapping_model.add_mapping(self.convert_tuple_to_mapping_data(data_tuple))
            self.update_all_views()

    @staticmethod
    def convert_tuple_to_mapping_data(data_tuple):
        # type: (Tuple[DragAndDropHeaderView.build_mime_data, DragAndDropHeaderView.build_mime_data]) -> dict
        """
        Convert raw drop event data into MappingDataModel mapping data
        :param data_tuple: <tuple> of form: (('Temp1', u'Blah', '1', 'Col1'), ('Output', 'NetSuite', '2', 'Id'))
                  meaning: (<template_type>, <template_name>, <column_index>, <column_name>)
        :return: <dict> of form {"Name": "", "Source Column": "", "Target Column": "", "In Data": "", "Out Data": ""}
        """
        mapping_data = {}
        source, target = data_tuple
        mapping_data[NAME_K] = '/'.join([target[0], target[1]])
        mapping_data[SOURCE_COLUMN_K] = source[-1]
        mapping_data[TARGET_COLUMN_K] = target[-1]
        mapping_data[IN_DATA_K] = datatypes.DataTypes.TEXT
        mapping_data[OUT_DATA_K] = datatypes.DataTypes.TEXT
        return mapping_data

    def on_new_template_clicked(self):
        if not self.dir_handler.get_existing_template_names()[OUTPUT_K]:
            menu = dialogs.ContextMenu(self, actions=('Output Template',))
        else:
            menu = dialogs.ContextMenu(self, actions=('Input Template', 'Output Template'))
        if menu.action == 'Input Template':
            self.template_creator.create_input_template()
        elif menu.action == 'Output Template':
            self.template_creator.create_output_template()

    def delete_selected_template(self):
        index = self.ui.tre_browse_templates.currentIndex()
        name = index.data()
        if name and name not in TEMPLATE_TYPES:
            the_path = self.ui.tre_browse_templates.model().filePath(index)
            result = dialogs.validation_message(
                'Warning', f'Are you sure you want to Permanently Delete "{name}"?   '
            )
            if result:
                for i in range(self.ui.tab_aliases.count()):
                    if self.ui.tab_aliases.tabText(i) == name:
                        self.ui.tab_aliases.removeTab(i)
                shutil.rmtree(the_path)

    def save_all_changes(self):
        widgets = self.findChildren(QtWidgets.QWidget)
        for w in widgets:
            try:
                model = w.model()
                model.save_data()
            except:
                pass

    def on_alias_tab_changed(self, tab=-1, name=None):  # type: (int, str) -> None
        if name:
            for i in range(self.ui.tab_aliases.count()):
                if self.ui.tab_aliases.tabText(i) == name:
                    self.ui.tab_aliases.setCurrentIndex(i)
                    tab = i
                    break
        if tab != -1 and not self.ui.grp_aliases.isHidden():
            self.save_mapping_changes()
            tab_name = self.ui.tab_aliases.tabText(tab)
            alias_data_files = self.dir_handler.get_alias_files(self.output_template.name, tab_name)
            if os.path.isfile(alias_data_files[MAPPINGS_K]):
                self.mapping_model.load_data(alias_data_files[MAPPINGS_K])
            self.update_all_views()

    def display_mapping_context_menu(self):
        menu = dialogs.ContextMenu(self, actions=('Move Up', 'Move Down', '_', 'Remove Selected'))
        index = self.ui.tbl_mappings.currentIndex()
        if menu.action == 'Move Up':
            self.mapping_model.move_row(index.row(), 1)
        elif menu.action == 'Move Down':
            self.mapping_model.move_row(index.row(), -1)
        elif menu.action == 'Remove Selected':
            if index.row() >= 0:
                result = dialogs.validation_message('Sure?', 'Delete selected Mapping?')
                if result:
                    self.mapping_model.delete_row(index.row())


if __name__ == '__main__':
    import sys
    from PySide2 import QtWidgets
    from csv_remapper.components.io_handlers import AppDirectoryHandler

    app = QtWidgets.QApplication(sys.argv)

    dialog = TemplateEditor('Template Editor', dir_handler=AppDirectoryHandler())
    dialog.showMaximized()

    sys.exit(app.exec_())
