'''
@author: oleg
'''
import os
import argparse

import ftapp.parsing.pars_util as pars_util
from ftapp.parsing.parse import Parser

import logging
logger = logging.getLogger(__name__)

pars_util.init_logging()

# process command line arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-c', action="store_true", default=False,
                    dest='console', help='if set output to the console (defaults to html output)')
args = arg_parser.parse_args()
console = args.console

TEST_DOCS = ['Calypso.txt', 'Lestrygonians.txt', 'LotusEaters.txt', 'Proteus.txt']

# process files
parser = Parser()
for file_n in TEST_DOCS:
    parser.load_file(file_n)
parser.clean_words()

if console:
    parser.display_res(pars_util.Output.CONSOLE)
else:
    #  create directory if doesn't exist
    out_dir = pars_util.OUTPUT_DIR
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    parser.display_res(pars_util.Output.BROWSER)
    print('see results in the "output" directory')
