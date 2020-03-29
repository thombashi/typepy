import re
from typing import Any


ansi_escape = re.compile(r"(\x9b|\x1b\[)[0-?]*[ -\/]*[@-~]", re.IGNORECASE)


def strip_ansi_escape(value: Any) -> str:
    return ansi_escape.sub("", value)
