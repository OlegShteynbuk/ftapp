'''
@author: oleg
'''
import os.path
from typing import Tuple, List
from enum import Enum
import re

import yaml
import logging
logger = logging.getLogger(__name__)

from jinja2 import Environment, FileSystemLoader

CONSOLE_HIGHL = ['\033[44;33m', '\033[m']
BROWSER_HIGHL = ['<span style="background-color:#00FFFF">', '</span>']

OUTPUT_DIR = 'output'
OUTPUT_FILE = 'ftapp.html'

class Output(Enum):
    CONSOLE = 1
    BROWSER = 2

class Highlighting():
    def __init__(self, higl_edg: Tuple[str, str]):
        self.h_start = higl_edg[0]
        self.h_end = higl_edg[1]

    def highlight_word(self, word: str) ->str:
        return self.h_start + word + self.h_end

    def higlight_sentence(self, sentence: str, words: List[str]) ->str:
        """
        args:
            sentence -
            words - words to highlight in the sentence

        return: the sentence with the words highlighted
        """
        start = 0
        sent_highl = ''
        for word in words:
            # find a word
            re_patt = fr"\b{word}\b"
            match = re.search(re_patt, sentence[start:], re.IGNORECASE)
            if match is None:
                # there should be a match
                logger.error(f'error finding a word {word} starting from position {start} in a sentence {sentence}')
                continue
            ind = match.start()
            if ind == -1:
                # the word should be found
                logger.error(f'error finding a word {word} starting from position {start} in a sentence {sentence}')
                continue
            # ind is a ralative index unlike string.find()
            ind = start + ind

            sent_highl += (sentence[start:ind] + self.highlight_word(word))
            # next word search start if needed
            start = ind + len(word)
        # add reminder of the sentence
        sent_highl += sentence[start:]

        return sent_highl


def display_browser(displ_w: List[str], display_info: List[Tuple]) -> None:
    """
    Create html file in the output directory from Jinja2 template

    args:
        displ_w - selected words
        display_info - text prepared for browser display
    """
    templates_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../templates')
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('table.html')

    # selected words
    sep = ', '
    words_h = sep.join(displ_w)

    template.stream(words=words_h, displ_i = display_info).dump(f'{OUTPUT_DIR}/{OUTPUT_FILE}')


DELIM =     '============================================================================='
DELIM_INT = '-----------------------------------------------------------------------------'
DELIM_BT  = '.............................................................................'
def display_console(displ_w: List[str], display_info: List[Tuple]) -> None:
    """
    print to the console, words highlighting can be displayed only in the console.
    if you want to save the results use output to html.

    args:
        displ_w - selected words
        display_info - text prepared for console display
    """
    print()
    print(DELIM)
    print()

    #selected words
    sep = ', '
    words_h = sep.join(displ_w)
    print(f'selected words: {words_h}')
    print()
    print(DELIM_INT)

    for w, count, docs, sents_h in display_info:
        print('      Word (Total Occurrences)')
        print(DELIM_BT)
        print(f'{w} ({count})')

        print(DELIM_BT)
        print('     Documents')
        print(DELIM_BT)
        sep = ', '
        docs = sep.join(docs)
        print(docs)

        print(DELIM_BT)
        print('      Sentences containing the word')
        print(DELIM_BT)
        for sent in sents_h:
            print(sent)
            print()

        print(DELIM_INT)
        print()

    print()
    print(DELIM)

def read_file(file_name: str) -> str:
    """
    read text file into memory, assuming that we have enough memory.

    args:
        file_name - file directory is relative, hardcoded to sampledocs
        display_info - text prepared for console display

    return: string with file's text
    """
    test_files_dir =  os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../sampledocs/')
    text_file = os.path.join(test_files_dir, file_name)

    with open(text_file, 'rt') as fin:
        astring = fin.read()
    return astring

def init_logging():
    """
    log files are in the working directory
    yaml file is in config directory, location is relative.
    """
    from logging.config import dictConfig

    config_file =  os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config/logging.yml')

    with open(config_file, 'rt') as f:
        config = yaml.safe_load(f.read())

    dictConfig(config)

    logger.info('logging initialized')
    logger.info(f'logging config_file - {config_file}')

if __name__ == '__main__':

    raise SystemExit()

