
from csv_remapper.components import (
    io_handlers,
    dialogs,
    datatypes,
)
from csv_remapper.constants import *


class TemplateCreator:
    def __init__(self, dir_handler):  # type: (io_handlers.AppDirectoryHandler) -> None
        self.dir_handler = dir_handler
        self.csv_handler = io_handlers.CsvFileHandler()
        self.json_handler = io_handlers.JsonFileHandler()

    def create_output_template(self):
        csv_file, name = None, None
        csv_file = dialogs.get_files_dialog(single_file=True)[0]
        if csv_file:
            name = dialogs.InputDialog(
                title='Output Template',
                mode=datatypes.InputMode.TEMPLATE_NAME,
                handler=self.dir_handler
            ).textValue()
        if all([csv_file, name]):
            self.dir_handler.create_template_folder(name, OUTPUT_K)
            template_files = self.dir_handler.get_template_files(name, OUTPUT_K)
            template_data = self.csv_handler.read(csv_file)
            self.csv_handler.write(template_files[FILE_K], template_data)
            return name
        return ''

    def create_input_template(self):
        csv_file, name, out_template = None, None, None
        csv_file = dialogs.get_files_dialog(single_file=True)[0]
        if csv_file:
            name = dialogs.InputDialog(
                title='Input Template',
                mode=datatypes.InputMode.TEMPLATE_NAME,
                handler=self.dir_handler
            ).textValue()
            if name:
                out_template = dialogs.InputDialog(
                    title='Input Template',
                    mode=datatypes.InputMode.SELECT_OUTPUT_TEMPLATE,
                    handler=self.dir_handler
                ).textValue()
        if all([csv_file, name, out_template]):
            self.dir_handler.create_template_folder(name, INPUT_K)
            template_files = self.dir_handler.get_template_files(name, INPUT_K)
            template_data = self.csv_handler.read(csv_file)
            mapping_data = {
                SOURCE_K: MAPPING_SEPARATOR.join([INPUT_K, name]),
                TARGET_K: MAPPING_SEPARATOR.join([OUTPUT_K, out_template]),
                MAPPINGS_K: []
            }
            self.csv_handler.write(template_files[FILE_K], template_data)
            self.json_handler.write(template_files[MAPPINGS_K], mapping_data)
            return name
        return ''

    def create_alias_data(self, template_name):  # type: (str) -> str
        name = dialogs.InputDialog(
            title='New Alias Data',
            mode=datatypes.InputMode.TEMPLATE_NAME,
            handler=self.dir_handler
        ).textValue()
        if name:
            self.dir_handler.create_alias_folder(template_name, name)
            alias_files = self.dir_handler.get_alias_files(template_name, name)
            alias_data = {HEADERS_K: [], DATA_K: []}
            mapping_data = {
                SOURCE_K: MAPPING_SEPARATOR.join([OUTPUT_K, template_name, name]),
                TARGET_K: MAPPING_SEPARATOR.join([OUTPUT_K, template_name]),
                LOOKUP_MODE_K: datatypes.LookupModes.MATCH_TEXT,
                MAPPINGS_K: []
            }
            self.csv_handler.write(alias_files[FILE_K], alias_data)
            self.json_handler.write(alias_files[MAPPINGS_K], mapping_data)
            return name
        return ''

    def create_alias_data_from_csv(self, template_name):  # type: (str) -> str
        name, csv_file = None, None
        csv_file = dialogs.get_files_dialog(single_file=True)[0]
        if csv_file:
            name = dialogs.InputDialog(
                title='New Alias Data',
                mode=datatypes.InputMode.TEMPLATE_NAME,
                handler=self.dir_handler
            ).textValue()
        if all([name, csv_file]):
            self.dir_handler.create_alias_folder(template_name, name)
            alias_files = self.dir_handler.get_alias_files(template_name, name)
            alias_data = self.csv_handler.read(csv_file)
            mapping_data = {
                SOURCE_K: MAPPING_SEPARATOR.join([OUTPUT_K, template_name, name]),
                TARGET_K: MAPPING_SEPARATOR.join([OUTPUT_K, template_name]),
                LOOKUP_MODE_K: datatypes.LookupModes.MATCH_TEXT,
                MAPPINGS_K: []
            }
            self.csv_handler.write(alias_files[FILE_K], alias_data)
            self.json_handler.write(alias_files[MAPPINGS_K], mapping_data)
            return name
        return ''
