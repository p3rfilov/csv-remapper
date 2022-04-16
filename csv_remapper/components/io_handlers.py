import csv
import json
import datetime
from typing import Any, List

from csv_remapper.components import decorators
from csv_remapper.constants import *


class FileHandler(object):
    def __init__(self):
        pass

    def read(self, the_file):
        raise NotImplemented

    def write(self, the_file, the_data):
        raise NotImplemented


class CsvFileHandler(FileHandler):
    def __init__(self):
        super(CsvFileHandler, self).__init__()

    @staticmethod
    @decorators.exception
    def read(csv_file):  # type: (str) -> dict
        """
        Read the contents of a CSV file
        :return: <dict> of form: ('headers': <list>, 'data': <list> of <dict>)
        """
        with open(csv_file, 'r', newline='', encoding='utf8') as f:
            _data = csv.reader(f, delimiter=CSV_DEFAULT_DELIMETER, quotechar=CSV_DEFAULT_QUOTECHAR)
            header_data = next(_data)
        with open(csv_file, 'r', newline='', encoding='utf8') as f:
            csv_data = csv.DictReader(f, delimiter=CSV_DEFAULT_DELIMETER, quotechar=CSV_DEFAULT_QUOTECHAR)
            data = {HEADERS_K: header_data, DATA_K: list(csv_data)}
        return data

    @staticmethod
    @decorators.exception
    def write(csv_file, data):  # type: (str, dict) -> None
        with open(csv_file, 'w', newline='', encoding='utf8') as f:
            writer = csv.DictWriter(f, fieldnames=data[HEADERS_K])
            writer.writeheader()
            writer.writerows(data[DATA_K])


class JsonFileHandler(FileHandler):
    def __init__(self):
        super(JsonFileHandler, self).__init__()

    @staticmethod
    @decorators.exception
    def read(the_file):  # type: (str) -> dict
        with open(the_file, 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    @decorators.exception
    def write(the_file, the_data):  # type: (str, dict) -> None
        with open(the_file, 'w') as f:
            json.dump(the_data, f, separators=(',', ': '), indent=2)


class AppDirectoryHandler:
    def __init__(self, root=None):  # type: (str) -> None
        self.handler = JsonFileHandler()
        self.root = root
        self.init_folders()

    def init_folders(self):
        self.create_folder(APP_SETTINGS_DIRECTORY)
        if not self.root:
            self.root = os.environ.get(APP_DATA_ENV_VAR) or self.get_settings(
                TEMPLATE_ROOT_DIR_K, DEFAULT_TEMPLATE_DIRECTORY
            )
        if self.root:
            for t_type in TEMPLATE_TYPES:
                self.create_folder(os.path.join(self.root, t_type))

    @decorators.exception
    def get_settings(self, key, fallback=''):  # type: (str, Any) -> Any
        if not os.path.exists(APP_SETTINGS_FILE):
            self.handler.write(APP_SETTINGS_FILE, {})
        data = self.handler.read(APP_SETTINGS_FILE)
        return data.get(key, fallback)

    @decorators.exception
    def write_settings(self, key, new_data):  # type: (str, Any) -> None
        if not os.path.exists(APP_SETTINGS_FILE):
            self.handler.write(APP_SETTINGS_FILE, {})
        data = self.handler.read(APP_SETTINGS_FILE)
        data[key] = new_data
        self.handler.write(APP_SETTINGS_FILE, data)

    def is_name_unique(self, name):  # type: (str) -> bool
        all_names = []
        t_names = self.get_existing_template_names()
        for t_type in TEMPLATE_TYPES:
            all_names += [t.lower() for t in t_names[t_type]]
        for list_item in t_names.values():
            for item in list_item:
                all_names += [t.lower() for t in self.get_alias_data_names(str(item))]
        if name.lower() not in set(all_names):
            return True
        return False

    def get_existing_template_names(self):
        templates = {}
        for t_type in TEMPLATE_TYPES:
            full_path = os.path.join(self.root, t_type)
            dirs = [d for d in os.listdir(full_path) if '.' not in d]
            templates[t_type] = sorted(dirs)
        return templates

    def get_alias_data_names(self, template_name):  # type: (str) -> List[str]
        full_path = os.path.join(self.root, OUTPUT_K, template_name)
        if os.path.isdir(full_path):
            dirs = [str(d) for d in os.listdir(full_path) if '.' not in d]  # bytes to string
            return sorted(dirs)
        return []

    def create_template_folder(self, name, template_type):  # type: (str, str) -> None
        full_path = os.path.join(self.root, template_type, name)
        self.create_folder(full_path)

    def create_alias_folder(self, template_name, name):  # type: (str, str) -> None
        full_path = os.path.join(self.root, OUTPUT_K, template_name, name)
        self.create_folder(full_path)

    def get_template_files(self, name, template_type):  # type: (str, str) -> dict
        full_path = os.path.join(self.root, template_type, name)
        return self._get_data_files(full_path, name)

    def get_alias_files(self, template_name, name):  # type: (str, str) -> dict
        full_path = os.path.join(self.root, OUTPUT_K, template_name, name)
        return self._get_data_files(full_path, name)

    def _get_data_files(self, the_path, name):  # type: (str, str) -> dict
        template_file = os.path.join(the_path, name + TEMPLATE_FORMAT)
        mappings = os.path.join(the_path, MAPPING_FILE)
        return {FILE_K: template_file, MAPPINGS_K: mappings}

    @decorators.exception
    def create_folder(self, folder):  # type: (str) -> None
        if not os.path.exists(folder):
            os.makedirs(folder)


def write_remapped_data(source_file, target_dir, remapped_data):  # type: (str, str, dict) -> str
    source_name = os.path.basename(source_file)
    name, ext = os.path.splitext(source_name)
    target_name = f'{name}{REMAPPED_SUFFIX}{datetime.datetime.now().strftime(DATETIME_FORMAT)}{ext}'
    target_file = os.path.join(target_dir, target_name)
    CsvFileHandler.write(target_file, remapped_data)
    return target_file
