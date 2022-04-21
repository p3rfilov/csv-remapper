
import re
from datetime import datetime
from dateutil import parser

from csv_remapper.components import (
    datatypes,
    io_handlers,
)
from csv_remapper.constants import *


def remap_csv_file(csv_file, out_template_name, dir_handler):  # type: (str, str, io_handlers.AppDirectoryHandler) -> dict
    input_csv_data = io_handlers.CsvFileHandler.read(csv_file)
    alias_data = _get_alias_data(out_template_name, dir_handler)
    out_temp_files = dir_handler.get_template_files(out_template_name, OUTPUT_K)  # cache output template files
    input_template_name = _get_input_template_name(csv_file, input_csv_data, out_template_name, dir_handler)
    in_temp_files = dir_handler.get_template_files(input_template_name, INPUT_K)

    # cache template data
    mapping_data = io_handlers.JsonFileHandler.read(in_temp_files[MAPPINGS_K])
    output_data = io_handlers.CsvFileHandler.read(out_temp_files[FILE_K])
    output_data[DATA_K] = []  # clear output data before populating it

    for row in input_csv_data[DATA_K]:
        skip_row = False
        output_row = {key: '' for key in output_data[HEADERS_K]}  # create empty data row
        for mapping in mapping_data[MAPPINGS_K]:
            if not skip_row:
                if mapping[SOURCE_COLUMN_K] not in row:
                    raise Exception(f'Invalid Mapping found: {mapping}')
                cell_data = row[mapping[SOURCE_COLUMN_K]]
                if cell_data.strip() and mapping[TARGET_COLUMN_K] in output_data[HEADERS_K]:
                    # only insert data that is present in the output template header
                    output_row[mapping[TARGET_COLUMN_K]] = _convert_value(
                        cell_data, mapping[IN_DATA_K], mapping[OUT_DATA_K]
                    )
                if mapping[TARGET_COLUMN_K] == ALIAS_FIELD_NAME:
                    # try to interpret the incoming data based on the alias lookup mode
                    match = None
                    alias_name = mapping[NAME_K].split(MAPPING_SEPARATOR)[-1]
                    if alias_name not in alias_data:
                        raise Exception('Please ensure a valid Output Template is selected')
                    data = alias_data[alias_name]
                    for a_data in data['csv'][DATA_K]:  # type: dict
                        # go through alias data row by row and return as soon as first match is found
                        if a_data[ALIAS_FIELD_NAME].strip() and cell_data.strip():
                            alias_strings = a_data[ALIAS_FIELD_NAME].split(ALIAS_DATA_SEPARATOR)
                            alias_strings = [s.lower() for s in alias_strings]
                            if data['json'][LOOKUP_MODE_K] == datatypes.LookupModes.MATCH_TEXT:
                                # try to find one of the aliases in 'cell_data'
                                if any([s in cell_data.lower() for s in alias_strings]):
                                    match = a_data
                                    break
                            elif data['json'][LOOKUP_MODE_K] == datatypes.LookupModes.MATCH_COL:
                                # multiple mappings expected; choose the first one with data in it
                                if any([s in mapping[SOURCE_COLUMN_K].lower() for s in alias_strings]):
                                    match = a_data
                                    break
                            elif data['json'][LOOKUP_MODE_K] == datatypes.LookupModes.OMIT_ROW:
                                # omit the row entirely if one of the aliases is found in 'cell_data'
                                if any([s in cell_data.lower() for s in alias_strings]):
                                    output_row = None
                                    skip_row = True
                                    break
                            elif data['json'][LOOKUP_MODE_K] == datatypes.LookupModes.REGEX:
                                # a single regular expression is expected in the Alias Data column
                                # choose the first one that returns a result
                                regex = a_data[ALIAS_FIELD_NAME]
                                result = _extract_substring(cell_data, regex)
                                if result:
                                    copy_data = a_data.copy()
                                    copy_data[ALIAS_FIELD_NAME] = result
                                    match = copy_data
                                    break
                    if match:
                        for a_mapping in data['json'][MAPPINGS_K]:
                            output_row[a_mapping[TARGET_COLUMN_K]] = _convert_value(
                                match[a_mapping[SOURCE_COLUMN_K]], a_mapping[IN_DATA_K], a_mapping[OUT_DATA_K]
                            )
        if output_row:
            output_data[DATA_K].append(output_row)
    return output_data


def _get_input_template_name(input_csv_file, input_csv_data, out_template_name, dir_handler):
    # type: (str, dict, str, io_handlers.AppDirectoryHandler) -> str
    """ Determine the Input template by looking at the input_csv_data header and output_template name """
    # There are 2 reasons the routine can fail:
    # 1. Input template for the given file type has not yet been defined
    # 2. Wrong or invalid Output template name

    all_template_files = {}
    all_templates = dir_handler.get_existing_template_names()

    for template_name in all_templates[INPUT_K]:  # check if an Input template with a given header exists
        template_files = dir_handler.get_template_files(template_name, INPUT_K)
        csv_data = io_handlers.CsvFileHandler.read(template_files[FILE_K])
        if csv_data[HEADERS_K] == input_csv_data[HEADERS_K]:
            all_template_files[template_name] = template_files  # cache template_files

    if not all_template_files:
        raise Exception(
            f'No Input Template could be found for file\n"{input_csv_file}".'
            f'\nPlease create New Input Template for this file type'
        )

    for template_name, template_files in all_template_files.items():  # check if Output template name is in the mappings
        mapping_data = io_handlers.JsonFileHandler.read(template_files[MAPPINGS_K])
        if mapping_data[TARGET_K].split(MAPPING_SEPARATOR)[-1] == out_template_name:
            return template_name
    raise Exception(f'Invalid Output Template "{out_template_name}" for file "{input_csv_file}"')


def _get_alias_data(output_template, dir_handler):  # type: (str, io_handlers.AppDirectoryHandler) -> dict[str, dict]
    """ Read all alias data files into a dictionary for a given output template """
    alias_data = {}
    alias_names = dir_handler.get_alias_data_names(output_template)
    for alias in alias_names:
        alias_files = dir_handler.get_alias_files(output_template, alias)
        alias_data[alias] = {
            'csv': io_handlers.CsvFileHandler.read(alias_files[FILE_K]),
            'json': io_handlers.JsonFileHandler.read(alias_files[MAPPINGS_K])
        }
    return alias_data


def _convert_value(value, in_type, out_type):  # type: (str, str, str) -> str
    if out_type == datatypes.DataTypes.NUM_POS:
        value = value.strip()
        if value.startswith('-'):
            return value[1:]
        return value
    elif out_type == datatypes.DataTypes.NUM_NEG:
        value = value.strip()
        if not value.startswith('-'):
            return '-' + value
        return value
    elif out_type.lower().startswith('date'):
        in_format = in_type.split()[-1]
        out_format = out_type.split()[-1]
        if in_type.lower().startswith('date'):
            return datetime.strptime(value, in_format).strftime(out_format)
        return parser.parse(value).strftime(out_format)
    return value


def _extract_substring(value, regex):  # type: (str, str) -> str
    result = re.search(regex, value)
    if result:
        return result.group(1)
    return ''
