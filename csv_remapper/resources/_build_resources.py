
import os

os.environ['COMPILE_PYSIDE2'] = 'True'
from csv_remapper.utils import build_resources

DIR = os.path.dirname(__file__)
build_resources.compile_pyside_ui_files(DIR)
