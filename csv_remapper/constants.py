
import os

APP_DATA_ENV_VAR = 'CSV_SETTINGS_DIR'

APP_NAME = 'CSV File Remapper'
APP_ICON = os.path.join(os.path.dirname(__file__), 'resources', 'Accounts-Icon.png')
APP_SETTINGS_DIRECTORY = os.environ.get(APP_DATA_ENV_VAR) or os.path.join(os.path.expanduser('~'), APP_NAME)
SETTINGS_FILE_NAME = 'settings.json'
APP_SETTINGS_FILE = os.path.join(APP_SETTINGS_DIRECTORY, SETTINGS_FILE_NAME)
DEFAULT_TEMPLATE_DIRECTORY = APP_SETTINGS_DIRECTORY
DEFAULT_BROWSE_DIR = os.path.expanduser('~')

# keys
INPUT_K = 'Input'
OUTPUT_K = 'Output'
NAME_K = 'Name'
SOURCE_COLUMN_K = 'Source Column'
TARGET_COLUMN_K = 'Target Column'
IN_DATA_K = 'In Data'
OUT_DATA_K = 'Out Data'
TEMPLATE_ROOT_DIR_K = 'root_folder'
MAPPINGS_K = 'mappings'
SOURCE_K = 'source'
TARGET_K = 'target'
LOOKUP_MODE_K = 'lookup_mode'
FILE_K = 'file'
HEADERS_K = 'headers'
DATA_K = 'data'

TEMPLATE_TYPES = (OUTPUT_K, INPUT_K)  # also used for widget insertion order

TEMPLATE_FORMAT = '.csv'
MAPPING_FILE = 'mappings.json'
MAPPING_SEPARATOR = '/'
NONE_STRING = '< None >'

REMAPPED_SUFFIX = '_remapped_'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M'

CSV_DEFAULT_DELIMETER = ','
CSV_DEFAULT_QUOTECHAR = '"'

ALIAS_FIELD_NAME = 'Alias Values'
ALIAS_DATA_SEPARATOR = '#'
ALIAS_TOOLTIP_TEXT = f' TIP: Use {ALIAS_DATA_SEPARATOR} character (without spaces) to separate ' \
                     f'"{ALIAS_FIELD_NAME}" values. Save Changes after adding new values to allow input validation'
ALIAS_REGEX_TOOLTIP_TEXT = ' TIP: When in Regular Expression mode, please only enter one value per row. ' \
                           f'No columns other than "{ALIAS_FIELD_NAME}" are required.'


# multiplier, based on current screen height and width
DATA_EDITOR_HEADER_ONLY_HEIGHT = 0.04
TEMPLATE_BROWSER_WIDTH = 0.12

COLOURS = {
    'dark_green': (10, 145, 0),
    'green': (180, 218, 174),
    'red': (196, 10, 10),
    'blue': (139, 188, 236),
}

# APP_FOLDER_STRUCTURE = {
#     'Input':
#     {
#         '<template_name>':
#         [
#             MAPPING_FILE,
#             '<parent.name>.csv',
#         ]
#     },
#     'Output':
#     {
#         '<template_name>':
#         [
#             MAPPING_FILE,
#             '<parent.name>.csv',
#             {
#                 '<alias_name>':
#                 [
#                     MAPPING_FILE,
#                     '<parent.name>.csv',
#                 ]
#             }
#         ]
#     },
# }
