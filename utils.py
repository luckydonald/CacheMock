def is_json_content_type(content_type: str) -> tuple[bool, bool]:
    """
    If it is a proper json content type, return True.
    >>> is_json_content_type("")
    False, False
    >>> is_json_content_type('application/json')
    True, False
    >>> is_json_content_type('json')
    True, False
    >>> is_json_content_type('application/json; charset=utf-8')
    True, False
    >>> is_json_content_type('application/x-ndjson; encoding=utf-8')
    True, True
    >>> is_json_content_type('application/x-ndjson')
    True, True
    >>> is_json_content_type('x-ndjson')
    True, True

    :param content_type:
    :return:
    """
    split = content_type.split(';')[0]
    split = split.lower()
    split = split.removeprefix('application/')
    split2 = split.removesuffix('x-nd')
    return split2 == 'json', split == 'x-ndjson'
# end def
