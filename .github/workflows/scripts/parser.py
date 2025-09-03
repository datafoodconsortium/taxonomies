#===============================================================================
#
#          FILE: parser.py
#   DESCRIPTION: JSON-LD parser.
#
#===============================================================================

import json

from typing import Dict

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

    @staticmethod
    def trim_id(id: str) -> str:
        id = id.removesuffix('#')
        if '#' in id:
            return id.split('#')[-1]
        elif '/' in id:
            return id.split('/')[-1].removesuffix('.rdf')
        elif ':' in id:
            return id.split(':')[-1]
        return id
