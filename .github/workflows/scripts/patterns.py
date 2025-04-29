#===============================================================================
#
#          FILE: patterns.py
#   DESCRIPTION: Regexp patterns for string validation.
#
#===============================================================================

from enum import Enum

class NamingPattern(Enum):
    ALPHANUM = (
        r'^(?:dfc-m:)?[a-zA-Z0-9]*$',
        "IDs must be alphanumeric"
    )
    LETTERFIRST = (
        r'^(?:dfc-m:)?[a-zA-Z].*$',
        "IDs must start with a letter"
    )
    PASCAL = (
        r'^(?:dfc-m:)?[A-Z][a-zA-Z0-9]*$',
        "Concepts must use PascalCase"
    )
    CAMEL = (
        r'^(?:dfc-m:)?[a-z][a-zA-Z0-9]*$',
        "Properties must use camelCase"
    )

    def __init__(self, pattern: str, message: str):
        self.pattern = pattern
        self.message = message
