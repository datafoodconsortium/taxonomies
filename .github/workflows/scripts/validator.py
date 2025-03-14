#===============================================================================
#
#          FILE: validator.py
#   DESCRIPTION: JSON-LD taxonomy validator.
#
#===============================================================================

import json
import re

from dataclasses import dataclass
from pathlib import Path
from typing import List

from parser import JSONLDParser
from patterns import NamingPattern

@dataclass
class ValidationError:
    message: str
    identifier: str = ""
    line: int = 0
    count: int = 1

class TaxonomyValidator:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.errors: List[ValidationError] = []
        
    def validate(self) -> bool:
        try:
            with open(self.file_path) as f:
                self.parser = JSONLDParser(f.read())
            return self._validate_graph()
        except json.JSONDecodeError as e:
            self.errors.append(
                ValidationError(f"Invalid JSON: {e.msg}", line=e.lineno)
            )
            return False

    def _validate_graph(self) -> bool:
        nodes = self.parser.get_nodes()
        valid = True
        for node in nodes:
            if not self._validate_node(node):
                valid = False
        return valid

    def _validate_node(self, node) -> bool:
        valid = True

        for k, v in node.items():
            is_property = ('@' not in k)
            is_id       = (k == '@id')
            is_concept  = any("Concept"  in t for t in node.get("@type", []))

            if is_property:
                valid = self._validate_property(k)
            elif is_id:
                valid = self._validate_id(v)
                if is_concept:
                    valid &= self._validate_concept(v)

        return valid

    def _validate_id(self, id) -> bool:
        id = self.parser.trim_id(id)
        return (
            self._match(NamingPattern.ALPHANUM, id) and
            self._match(NamingPattern.LETTERFIRST, id)
        )

    def _validate_concept(self, concept) -> bool:
        id = self.parser.trim_id(concept)
        return self._match(NamingPattern.PASCAL, id)

    def _validate_property(self, property) -> bool:
        id = self.parser.trim_id(property)
        return self._match(NamingPattern.CAMEL, id)

    def _match(self, naming_pattern, id) -> bool:
        if not re.match(naming_pattern.pattern, id):
            line = self.parser.get_line_number(id)
            self._append_error(ValidationError(
                naming_pattern.message, id, line
            ))
            return False
        return True

    def _append_error(self, new: ValidationError):
        found = False
        for e in self.errors:
            if f"{new.message}{new.identifier}" == f"{e.message}{e.identifier}":
                e.count += 1
                found = True
        if not found:
            self.errors.append(new)

    def print_errors(self):
        for e in sorted(self.errors, key=lambda e: e.line):
            message  = f"    [L{e.line}]\t{e.message}"
            message += f"\t- in '{e.identifier}'"
            if e.count > 1:
                message += f" ({e.count} occurences)"
            print(message)
        print()

    def get_errors_count(self) -> int:
        return sum(e.count for e in self.errors)
