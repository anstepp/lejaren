from re import search

from lxml import etree

from ..notation.score import Score

class inputParser:

    def __init__(self) -> inputParser:
        pass

    def set_input(self, input: str) -> None:
        if not isinstance(input, str):
            raise TypeError(f'File must me string, is: {input}', input)
            return False #testing
        self.input = input
        return True #testing

    def clean_input(self, input):
        # TODO: Verify an xml input file is actaully MusicXML
        cleaned_input = search(r'.*\.musicxml$|\.mxl$|\.xml$', input)
        if not cleaned_input:
            raise ValueError(f'File must be music xml, but is {input}', input)
        else:
            return input

    def _create_tree(self, input):
        tree = etree.parse(input)
        return Score(tree)