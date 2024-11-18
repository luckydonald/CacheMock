from typing import Literal


def is_json_content_type(content_type: str) -> Literal['json', 'json-lines', '']:
    """
    If it is a proper json content type, return True.
    >>> is_json_content_type("")
    ''
    >>> is_json_content_type('application/json')
    'json'
    >>> is_json_content_type('json')
    'json'
    >>> is_json_content_type('application/json; charset=utf-8')
    'json'
    >>> is_json_content_type('application/x-ndjson; encoding=utf-8')
    'json-lines'
    >>> is_json_content_type('application/x-ndjson')
    'json-lines'
    >>> is_json_content_type('x-ndjson')
    'json-lines'

    :param content_type:
    :return:
    """
    split = content_type.split(';')[0]
    split = split.lower()
    split = split.removeprefix('application/')
    if split == 'json':
        return 'json'
    # end if
    if split == 'x-ndjson':
        return 'json-lines'
    # end if
    return ''
# end def
