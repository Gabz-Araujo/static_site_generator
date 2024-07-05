from enum import Enum


class InlineDelimiters(Enum):
    TEXT = ""
    BOLD = ("__", "**")
    ITALIC = ("_", "*")
    CODE = "`"
