
import os
import subprocess
from glob import glob
from collections import OrderedDict

PS1_COMPILERS = {
    '.ui': 'pyside-uic',
    '.qrc': 'pyside-rcc',
}
PS2_COMPILERS = {
    '.ui': 'pyside2-uic',
    '.qrc': 'pyside2-rcc',
}
FILE_COMPILER_TYPES = PS1_COMPILERS
if os.environ.get('COMPILE_PYSIDE2'):  # for PySide2, set this env var before importing this module
    print('Using PySide2 compilers.')
    FILE_COMPILER_TYPES = PS2_COMPILERS


def get_supported_files(directory=os.getcwd()):
    files = []
    for ext, comp in FILE_COMPILER_TYPES.items():
        files.extend(glob(os.path.join(directory, '*' + ext)))
    return files


def compile_pyside_ui_files(directory=os.getcwd()):
    files = get_supported_files(directory)
    for f in files:
        file_path, ext = os.path.splitext(f)
        py_file = file_path + '.py'
        cmd = [FILE_COMPILER_TYPES[ext], f, '-o', py_file]
        print(f'Running command: {cmd}')
        build = subprocess.Popen(cmd)
        build.wait()


def pyside_one_to_qt(directory=os.getcwd(), resource_only=False):
    replace_lines = OrderedDict()
    if not resource_only:
        replace_lines['from PySide'] = '''
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *

'''
    replace_strings = OrderedDict()
    if not resource_only:
        replace_strings['QtGui.'] = ''
        replace_strings['QtCore.'] = ''
        replace_strings[', QApplication.UnicodeUTF8'] = ''
    replace_strings['_qrc_rc'] = '_qrc'  # all resource files should have _qrc prefix
    _replace_file_contents(directory, replace_lines, replace_strings)


def pyside_two_to_qt(directory=os.getcwd(), resource_only=False, rep_lines=OrderedDict(), rep_strings=OrderedDict()):
    replace_lines = rep_lines
    replace_strings = rep_strings
    if not resource_only:
        replace_strings['from PySide2'] = 'from Qt'
    replace_strings['_qrc_rc'] = '_qrc'  # all resource files should have _qrc prefix
    _replace_file_contents(directory, replace_lines, replace_strings)


def _replace_file_contents(directory, replace_lines, replace_strings):
    def _read_file(the_file):
        with open(the_file) as f:
            return f.readlines()

    def _write_file(the_file, line_list):
        the_string = ''.join(line_list)
        with open(the_file, 'w') as f:
            f.write(the_string)

    files = get_supported_files(directory)
    for f in files:
        py_file = os.path.splitext(f)[0] + '.py'
        if os.path.isfile(py_file):
            edited_lines = []
            lines = _read_file(py_file)
            for line in lines:
                for key, val in replace_lines.items():
                    if key in line:
                        line = val
                for key, val in replace_strings.items():
                    line = line.replace(key, val)
                edited_lines.append(line)
            _write_file(py_file, edited_lines)
