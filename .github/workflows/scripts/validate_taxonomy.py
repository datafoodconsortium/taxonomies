#===============================================================================
#
#          FILE: validate_taxonomy.py
#
#         USAGE: python validate_taxonomy.py <json_ld_file>
#
#   DESCRIPTION: Validates JSON-LD taxonomies following DFC naming conventions:
#                - Must be valid JSON-LD
#                - IDs must be alphanumeric
#                - IDs must start with a letter
#                - Classes use PascalCase
#                - Properties use camelCase
#
#===============================================================================

from dataclasses import dataclass
from collections import Counter
from enum import Enum
from pathlib import Path
import json
import re
import sys
from typing import List, Dict

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

@dataclass
class ValidationError:
    message: str
    identifier: str = ""
    line: int = 0
    count: int = 1

class JSONLDParser:
    def __init__(self, content: str):
        self.content = content
        self.id_lines = self._map_ids_to_lines()
        self.data = json.loads(content)

    def _map_ids_to_lines(self) -> Dict[int, str]:
        return {
            line_num: line 
            for line_num, line in enumerate(self.content.split('\n'), 1)
        }

    def _get_graph(self) -> list:
        if '@graph' in self.data:
            return self.data['@graph']
        elif isinstance(self.data, list):
            return next((i['@graph'] for i in self.data if '@graph' in i), [])

    def get_nodes(self) -> list:
        nodes = []
        stack = [self._get_graph()]

        while stack:
            current = stack.pop()
            if isinstance(current, dict):
                nodes.append(current)
                stack.extend(current.values())
            elif isinstance(current, list):
                stack.extend(current)
        
        return nodes

    def get_line_number(self, id: str) -> int:
        return next((num for num, line in self.id_lines.items()
                    if id in line), 0)

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
        id = self._trim_id(id)
        return (
            self._match(NamingPattern.ALPHANUM, id) and
            self._match(NamingPattern.LETTERFIRST, id)
        )

    def _validate_concept(self, concept) -> bool:
        id = self._trim_id(concept)
        return self._match(NamingPattern.PASCAL, id)

    def _validate_property(self, property) -> bool:
        id = self._trim_id(property)
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

    @staticmethod
    def _trim_id(id: str) -> str:
        id = id.removesuffix('#')
        if '#' in id:
            return id.split('#')[-1]
        elif '/' in id:
            return id.split('/')[-1].removesuffix('.rdf')
        elif ':' in id:
            return id.split(':')[-1]
        return id

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_taxonomy.py <json_ld_file>")
        sys.exit(1)

    tv = TaxonomyValidator(sys.argv[1])
    if tv.validate():
        print(f"\n✨ PASS {tv.file_path.name} is valid!")
        sys.exit(0)

    errors_count = sum(e.count for e in tv.errors)
    print(f"\n❌ FAIL Found {errors_count} issues in {tv.file_path.name}:\n")

    for e in sorted(tv.errors, key=lambda e: e.line):
        message  = f"    [L{e.line}]\t{e.message}"
        message += f"\t- in '{e.identifier}'"
        if e.count > 1:
            message += f" ({e.count} occurences)"
        print(message)
    sys.exit(1)

if __name__ == "__main__":
    main()