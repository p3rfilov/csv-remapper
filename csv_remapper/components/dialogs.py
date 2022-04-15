
import re
from PySide2 import QtWidgets, QtGui, QtCore

from csv_remapper.components import io_handlers, datatypes
from csv_remapper.constants import *

# noinspection PyUnreachableCode
if False:
    from typing import Iterable, List, Optional
    from csv_remapper.components.models import CsvDataModel


def validation_message(tile, message, buttons=True):  # type: (str, str, bool) -> bool
    dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, tile, message)
    yes = None
    if buttons:
        yes = dialog.addButton('Yes', QtWidgets.QMessageBox.YesRole)
        dialog.addButton('No', QtWidgets.QMessageBox.NoRole)
    dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    dialog.exec_()
    reply = dialog.clickedButton()

    if reply == yes:
        return True
    return False


def get_directory_dialog(parent=None, title='Select Folder'):  # type: (QtCore.QObject, str) -> str
    directory = QtWidgets.QFileDialog.getExistingDirectory(parent, title, DEFAULT_BROWSE_DIR)
    return directory


def get_files_dialog(parent=None, title='Select File(s)', single_file=False, file_types=(f'*{TEMPLATE_FORMAT}',)):
    # type: (QtCore.QObject, str, bool, Iterable[str]) -> List[str]
    file_filter = f'Files ({" ".join(file_types)})'
    if single_file:
        one_file = QtWidgets.QFileDialog.getOpenFileName(parent, title, DEFAULT_BROWSE_DIR, file_filter)
        files = [[one_file[0]]]
    else:
        files = QtWidgets.QFileDialog.getOpenFileNames(parent, title, DEFAULT_BROWSE_DIR, file_filter)
    return files[0]


def save_file_dialog(parent=None, title='Save File As...', file_type=f'*{TEMPLATE_FORMAT}'):
    # type: (QtCore.QObject, str, str) -> str
    file_path = QtWidgets.QFileDialog.getSaveFileName(parent, title, DEFAULT_BROWSE_DIR, file_type)
    return file_path[0]


class ContextMenu(QtWidgets.QMenu):
    def __init__(self, parent=None, actions=('Yes', 'No')):
        # type: (QtCore.QObject, Iterable[str]) -> None
        """
        Customizable context menu that returns the name of the clicked action.
        Action property returns <None> if no action is selected.
        Usage:
            menu = ContextMenu(actions=('Default', 'V-Ray'))
            renderer = menu.action
        """
        super(ContextMenu, self).__init__(parent)
        self._action_name = None
        for action in actions:
            if action == '_':
                self.addSeparator()
            else:
                self.addAction(action, self._action_clicked)
        self._show()

    @property
    def action(self):  # type: () -> Optional[str]
        return self._action_name

    def _action_clicked(self):
        self._action_name = self.sender().text()

    def _show(self):
        self.exec_(QtGui.QCursor.pos())


class InputDialog(QtWidgets.QInputDialog):
    def __init__(self, mode, handler, title=NAME_K, label='', parent=None, model=None):
        # type: (datatypes.InputMode, io_handlers.AppDirectoryHandler, str, str, QtCore.QObject, CsvDataModel) -> None
        super(InputDialog, self).__init__(parent)
        self.setWindowTitle(title)
        self.label = label
        self.handler = handler
        self.mode = mode
        self.parent = parent
        self.model = model
        self.setInputMode(QtWidgets.QInputDialog.TextInput)
        self.setModal(True)

        self.set_dialog_options()
        self.show()
        self.exec_()  # don't return until closed

    def set_dialog_options(self):
        if self.mode == datatypes.InputMode.COLUMN_NAME:
            self.setLabelText(self.label or 'Please enter Column Name')
        elif self.mode == datatypes.InputMode.TEMPLATE_NAME:
            self.setLabelText(self.label or 'Please enter Template Name')
        elif self.mode == datatypes.InputMode.SELECT_OUTPUT_TEMPLATE:
            self.setLabelText(self.label or 'Please choose Output Template')
            templates = self.handler.get_existing_template_names()[OUTPUT_K]
            if not templates:
                validation_message('Error', 'No Output Templates found!', buttons=False)
                raise Exception('No Output Templates found!')
            self.setComboBoxItems(templates)
        elif self.mode == datatypes.InputMode.TABLE_COLUMN:
            self.setLabelText(self.label or 'Please choose Column with unique values (IDs)')
            self.setComboBoxItems([NONE_STRING] + self.model.columns)  # add None as first option

    def input_valid(self):
        if not self._validate_text():
            return False
        elif self.mode == datatypes.InputMode.COLUMN_NAME and not self._validate_column_name():
            return False
        elif self.mode == datatypes.InputMode.TEMPLATE_NAME and not self._validate_template_name():
            return False
        return True

    def _validate_text(self):
        text = self.textValue()
        if text and re.match(r'^[A-Za-z0-9_ ]*$', text) or text in (NONE_STRING,):
            return True
        validation_message('Illegal characters found', 'Please use only Letters and Numbers.', buttons=False)
        return False

    def _validate_column_name(self):
        if not self.model or not hasattr(self.model, 'columns'):
            validation_message('Error', 'No valid Model provided!', buttons=False)
            raise Exception('No valid Model provided!')
        text = self.textValue().lower()
        columns = [c.lower() for c in self.model.columns]
        if text in columns:
            validation_message(
                'Name Not Unique', 'This Column already exists. Please choose another Name',
                buttons=False
            )
            return False
        return True

    def _validate_template_name(self):
        text = self.textValue().lower()
        if text in [t.lower() for t in TEMPLATE_TYPES]:
            validation_message('Name Not Valid', f'Names {TEMPLATE_TYPES} are reserved.', buttons=False)
            return False
        elif not self.handler.is_name_unique(text):
            validation_message(
                'Name Not Unique', 'This Template already exists. Please choose another Name.',
                buttons=False
            )
            return False
        return True

    def done(self, result):
        if not result or self.input_valid():
            if not result:
                self.setTextValue('')
            super(InputDialog, self).done(result)


if __name__ == '__main__':
    import sys
    from PySide2 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)

    d = InputDialog(datatypes.InputMode.TEMPLATE_NAME, io_handlers.AppDirectoryHandler())
    print(d.textValue())
    d = get_directory_dialog()
    print(d)
    d = get_files_dialog()
    print(d)
