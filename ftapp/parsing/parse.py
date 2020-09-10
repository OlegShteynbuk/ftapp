'''
@author: oleg
'''
from collections import defaultdict
from collections import Counter
from typing import Tuple, List

import nltk
from nltk.corpus import stopwords

import ftapp.parsing.pars_util as pars_util

import logging
logger = logging.getLogger(__name__)

WORDS_NOT_INTERESTED = ['day', 'eye', 'hand', 'time', 'second', 'thing',  'air', 'water', 'home', 'foot', 'weight', 'sun']
WORDS_INTERESTED_LIMIT = 2

class Parser():
    def __init__(self):
        # associate a word with a file and a sentence in the file;
        # if memory is an issue can trade speed for memory by
        # keeping a sentence position in the file instead of a sentence and re-reading and re-processing the file,
        # then will need memory for the largest of the files.
        self.words_d = defaultdict(list)
        self.words_c = Counter()

    def load_file(self, file_n: str):
        """
        args:
            file_n - file to load
        """
        try:
            sentences_t = pars_util.read_file(file_n)
        except:
            logger.error(f'{file_n} will not be processed, exception reading the file. ', exc_info=True)
            return

        sentences = nltk.tokenize.sent_tokenize(sentences_t)
        for sentence in sentences:
            _, words_lem = Parser.prepare_sentence(sentence)

            #  another Counter to avoid repeating an entry in words_d when the same word appears twice or more in a sentence.
            tmp_counter = Counter(words_lem)
            for word, count in tmp_counter.items():
                # associate a word with the file and the sentence
                self.words_d[word].append((file_n, sentence))
                # count words
                self.words_c[word] += count

    def clean_words(self):
        """
        Remove uninteresting words.

        After each run, if you don't like the top choices just add them to WORDS_NOT_INTERESTED.
            Can we say poor man's training a model?
        """
        for k in WORDS_NOT_INTERESTED:
            self.words_c.pop(k, None)

    def display_res(self, output: pars_util.Output):
        """
        args:
            output - whether for console or browser
        """
        if output is pars_util.Output.CONSOLE:
            highlighter = pars_util.Highlighting(pars_util.CONSOLE_HIGHL)
        else:
            highlighter = pars_util.Highlighting(pars_util.BROWSER_HIGHL)

        display_info = []
        interesting_w = self.words_c.most_common(WORDS_INTERESTED_LIMIT)
        for wc in interesting_w:
            # get words and counts
            w = wc[0]
            count = wc[1]

            # prepare sentences
            sents_h  = []     # sentences with highlighted words
            docs = set()
            #  to correctly highlight the word we need the word as it is in the text
            #   (the word that we have now is after lemmatization as we need to count all forms of the word)
            for file_n, sentence in self.words_d[w]:
                docs.add(file_n)
                # can trade memory for speed by keeping words_filterd and words_lem in the dictionary along with the sentence
                words_filterd, words_lem = Parser.prepare_sentence(sentence)
                inds = [i for i, x in enumerate(words_lem) if x == w]
                # get the words as they appear in the text(before lemmatization)
                words = [words_filterd[i] for i in inds]

                # highlight sentence
                sent_highl = highlighter.higlight_sentence(sentence, words)
                sents_h.append(sent_highl)

            # prepare docs
            docs = sorted(list(docs))

            display_info.append((w, count, docs, sents_h))

        # higlight words for the selected words display
        displ_w = [wc[0] for wc in interesting_w]
        displ_w = [highlighter.highlight_word(w) for w in displ_w]

        #     output
        if output is pars_util.Output.CONSOLE:
            pars_util.display_console(displ_w, display_info)
        else:
            pars_util.display_browser(displ_w, display_info)

    @staticmethod
    def prepare_sentence(sentence: str) -> Tuple[List, List]:
        """
        break sentence into tokens, filter tokens, and lemmatize tokens

        return: filtered tokens and lemmatized tokens
        """
        stop_words = set(stopwords.words('english'))

        tagged_sent = nltk.pos_tag(nltk.tokenize.word_tokenize(sentence))

        # remove proper names,  convert to lower case;
        # assuming that after filtering for proper names can safely convert to lower case.
        words_filterd = [word.lower() for word,pos in tagged_sent if pos != 'NNP' and pos.startswith('NN')]
        # stopwords removal, for performance, otherwise not needed
        words_filterd = [w for w in words_filterd if w not in stop_words]

        # lemmatize
        wnl = nltk.stem.wordnet.WordNetLemmatizer()
        words_lem = [wnl.lemmatize(t) for t in words_filterd]

        return words_filterd, words_lem


if __name__ == '__main__':

    # manual highlighting test
    sentence = 'Thursday is the day of the days a beautiful day'
    words = ['day', 'days', 'day']
    highlighter = pars_util.Highlighting(pars_util.CONSOLE_HIGHL)
    sent_highl = highlighter.higlight_sentence(sentence, words)
    print(sent_highl)


    raise SystemExit()
