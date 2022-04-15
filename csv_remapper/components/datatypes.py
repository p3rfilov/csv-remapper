
import enum


class BaseStrEnum(str, enum.Enum):
    def __str__(self):
        return str.__str__(self)

    @classmethod
    def all(cls):
        return list(map(str, cls))


class InputMode(enum.Enum):
    COLUMN_NAME = enum.auto()
    TEMPLATE_NAME = enum.auto()
    SELECT_OUTPUT_TEMPLATE = enum.auto()
    TABLE_COLUMN = enum.auto()


class LookupModes(BaseStrEnum):
    MATCH_TEXT = 'Match Text (substring; case-insensitive)'
    MATCH_COL = 'Match Column Name (chooses first column with data in it)'
    OMIT_ROW = 'Omit Row with Text'
    REGEX = 'Regular Expression (extract value)'


class DataTypes(BaseStrEnum):
    TEXT = 'Text'
    NUM_POS = '+ Number'
    NUM_NEG = '- Number'
    DATE_DMY_S = 'Date %d/%m/%Y'
    DATE_MDY_S = 'Date %m/%d/%Y'
    DATE_YMD_S = 'Date %Y/%m/%d'
    DATE_DMY_H = 'Date %d-%m-%Y'
    DATE_MDY_H = 'Date %m-%d-%Y'
    DATE_YMD_H = 'Date %Y-%m-%d'
    DATE_DMY_D = 'Date %d.%m.%Y'
    DATE_MDY_D = 'Date %m.%d.%Y'
    DATE_YMD_D = 'Date %Y.%m.%d'


if __name__ == '__main__':
    print(DataTypes.TEXT)
    print(DataTypes.all())
