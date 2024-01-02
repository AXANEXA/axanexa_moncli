from importlib import import_module

from .constants import *
from .objects import *
from .base import *
from .simple import *
from .complex import *
from .readonly import *


def create_column_value(column_type: ColumnType, **kwargs):
    """Create column value instance

    Parameters

        column_type : `moncli.ColumnType`
            The column type to create.
        kwargs : `dict`
            The raw column value data.
    """
    kwargs=convert_dicts(kwargs) 
    return getattr(
        import_module(__name__), 
        COLUMN_TYPE_VALUE_MAPPINGS.get(column_type, 'ReadonlyValue'))(**kwargs)

def convert_dicts(input_dict):
    result_dict = {
        "id": input_dict['id'],        'additional_info': ''  # You can set the appropriate value for additional_info
    }
    if 'text' in input_dict:
        result_dict['text'] = input_dict['text']
    if 'value' in input_dict:
        result_dict['value'] = input_dict['value']
    if 'settings_str' in input_dict:
        result_dict['settings_str'] = input_dict['settings_str']
    if 'title' in input_dict:
        result_dict['title'] = input_dict['title']
    if 'type' in input_dict:
        result_dict['type'] = input_dict['type']
    if 'width' in input_dict:
        result_dict['width'] = input_dict['width']
    if 'archived' in input_dict:
        result_dict['archived'] = input_dict['archived']
    if 'column' in input_dict and 'title' in input_dict['column']:
        result_dict['title'] = input_dict['column']['title']
    if 'description' in input_dict:
        result_dict['description'] = input_dict['description']

    return result_dict