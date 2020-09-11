# First Text Analysis Python Project
The goal of this project is to extract information from text documents by displaying a list of the most frequent words that fall under certain criteria, along with the document names and sentences where those words appear. This project could be used as a starting point for a text analysis project. The text samples are the beginnings of several chapters from Ulysses. The original project had different text samples which for various reasons we can't open source, and chapters from Ulysses were chosen because we are big Joyce fans.

## Trade offs
* In this implementation the criteria for word selection will be nouns minus proper names. The words selection can be  adjusted by modifying the list of words that we do not want to select. After each run if you don't like the top choices just add them to the list. Another approach could be to create a list of words that we want to select.
* There is a constant to limit the number of words to display.
* If html output selected(default) the output will be in the 'output' folder
* The program should have enough memory for the largest of the documents. There are various techniques to deal with big files; processing big files is not implemented yet. Current implementation read all files into memory; there are comments in the code how to change the code to keep in memory one file at a time.
* It is possible to trade speed for memory and vice versa, see comments in the code.
* Log files are in the working directory. Because the results can be displayed in the console there is no console logger.

## Prerequisites
* The program was tested on Linux with Python 3.7, nltk 3.5, jinja2 2.11, pytest 6.0, pyyaml 5.3.
* The console output was tested with Bash shell, and html output was tested with Chrome and Firefox.

## Installing
* create directory and unzip or clone the project, it will be the project root directory
* cd to the project root directory.
* create a virtual environment from conda-req.txt, which is located in the requirements directory; conda-req.txt was created by conda.
* init nltk installation, this step is optional depending on nltk installation
python ./ftapp/parsing/init_installation.py

## Running
	python -m ftapp.parsing.process
	  optional arguments:
	  	-h, --help  (show help message)
	  	-c  (output to the console, defaults to html output)

## Running the tests
	python -m pytest ftapp/tests
		or
	python -m pytest ftapp/tests/test_parse.py


