from re import search

from lxml import etree

import lejaren.notation as ljn

class inputParser:

    def __init__(self, input: str) -> inputParser:
        if not isinstance(input, str):
            raise TypeError(f'File must me string, is: {input}', input)
        self._clean_input(input)
        self.input = input

    def _clean_input(self, input):
        # TODO: Verify an xml input file is actaully MusicXML
        cleaned_input = search(r'.*\.musicxml$|\.mxl$|\.xml$', input)
        if not cleaned_input:
            raise ValueError(f'File must be music xml, but is {input}', input)
        else:
            return input

    def create_tree():
        tree = etree.parse(input)
        return ljn.Score(tree)