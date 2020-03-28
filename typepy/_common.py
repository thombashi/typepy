import re


ansi_escape = re.compile(r"(\x9b|\x1b\[)[0-?]*[ -\/]*[@-~]", re.IGNORECASE)


def strip_ansi_escape(value):
    return ansi_escape.sub("", value)
