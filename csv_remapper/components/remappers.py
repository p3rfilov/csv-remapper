
import re
from datetime import datetime
from dateutil import parser

from csv_remapper.components import (
    datatypes, 
    dialogs, 
    io_handlers,
)
from csv_remapper.constants import *


def remap_csv_file(csv_file, output_template, dir_handler):  # type: (str, str, io_handlers.AppDirectoryHandler) -> dict
    output_data = {}
    input_data = io_handlers.CsvFileHandler.read(csv_file)
    in_temp_data = {}
    alias_data = _get_alias_data(output_template, dir_handler)
    input_template = None
    in_temp_files = None

    # cache output template data
    out_temp_files = dir_handler.get_template_files(output_template, OUTPUT_K)

    # determine input template
    all_templates = dir_handler.get_existing_template_names()
    for name in all_templates[INPUT_K]:
        in_temp_files = dir_handler.get_template_files(name, INPUT_K)
        in_temp_data['csv'] = io_handlers.CsvFileHandler.read(in_temp_files[FILE_K])
        if in_temp_data['csv'][HEADERS_K] == input_data[HEADERS_K]:
            input_template = name
            break

    if input_template:
        # cache template data
        in_temp_data['json'] = io_handlers.JsonFileHandler.read(in_temp_files[MAPPINGS_K])
        output_data = io_handlers.CsvFileHandler.read(out_temp_files[FILE_K])
        output_data[DATA_K] = []  # clear output data before populating it

        for row in input_data[DATA_K]:
            skip_row = False
            output_row = {key: '' for key in output_data[HEADERS_K]}  # create empty data row
            for mapping in in_temp_data['json'][MAPPINGS_K]:
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
    else:
        dialogs.validation_message(
            'Unknown File Template',
            'Input Template not defined. Please create New Input Template for this file type.\n'
            f'File: {csv_file}',
            buttons=False
        )
    return output_data


def _get_alias_data(output_template, dir_handler):
    alias_data = {}
    alias_names = dir_handler.get_alias_value_names(output_template)
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
