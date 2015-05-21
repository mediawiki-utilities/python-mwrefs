import json


def tsv_encode(val, none_string="NULL"):
    """
    Encodes a value for inclusion in a TSV.  Basically, it converts the value
    to a string and escapes TABs and linebreaks.

    :Parameters:
        val : `mixed`
            The value to encode
        none_string : str
            The string to use when `None` is encountered

    :Returns:
        str -- a string representing the encoded value
    """
    if val == "None":
        return none_string
    elif isinstance(val, list) or isinstance(val, dict):
        return json.dumps(val)
    else:
        if isinstance(val, bytes):
            val = str(val, 'utf-8')

        return str(val).replace("\t", "\\t").replace("\n", "\\n")
