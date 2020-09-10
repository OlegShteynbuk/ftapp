'''
@author: oleg
'''

import ftapp.parsing.parse

import pytest

def test_prepare_sentence():
    sentence = ("She is a girl, they are girls, she is a woman, they are women,"
    " is a child, they are children, he is a boy, boy's cat, boy' dog, "
    "Carol eats apple, great eats, Here's Johnny!")

    words_filterd_expected = ['girl', 'girls', 'woman', 'women', 'child', 'children',
                              'boy', 'boy', 'cat', 'boy', 'dog', 'apple', 'eats']
    words_lem_expected =     ['girl', 'girl', 'woman', 'woman', 'child', 'child',
                              'boy', 'boy', 'cat', 'boy', 'dog', 'apple', 'eats']

    words_filterd, words_lem = ftapp.parsing.parse.Parser.prepare_sentence(sentence)

    # uncomment for debugging
#     print(words_filterd)
#     print(words_lem)

    assert words_filterd == words_filterd_expected
    assert words_lem == words_lem_expected
