#!/usr/bin/env python3.9

"""
Module containing functions for readability of text as well as
containing a main block that calculates the SMOG grade of a given
amount of text from standard input when run as a script.
"""

__author__ = "Vin Clover, vclover@jeff.cis.cabrillo.edu"

import math
import sys
import re

_syllables = dict()


def _load_syllable_data():
    """
    Populates '_syllables' dictionary with info from
    '/srv/datasets/syllables.txt' with lowercase words
    as keys and lists of lowercase syllable strings as values.
    """
    with open("/srv/datasets/syllables.txt") as file:
        for line in file:
            _syllables[line.lower().strip().replace(";", "")] = line.strip().lower().split(";")


_load_syllable_data()  # Populates _syllables dictionary upon import of module


def syllables(word):
    """
    Receives string input in the form of a single case-insensitive word and checks it against the
    _syllables dictionary.  If the word exists in the dictionary, it returns a list of the
    syllables in that word.  Otherwise, it returns a list with a single entry of the
    unmatched word.
    """
    if word.lower() in _syllables:
        return _syllables[word.lower()]
    else:
        return [word]


def words(full_text_input):
    """
    Receives text input of any size and returns a list of the individual words
    in that text.
    """
    # Splits words apart
    # Removes leading and trailing apostrophes and hyphens.
    words_list = [
        word.strip("'-")
        for word in re.split("[^A-Za-z'-]", full_text_input)
        if word.strip("'-") != ""
    ]

    return words_list


def sentences(full_text_input):
    """
    Receives string input of any size and returns a list of lists containing the individual
    words within a sentence, separated by individual sentences.
    """
    sentence = []
    sentences_list_of_word_lists = []
    start_quotes = False
    end_quotes = False
    # Creates list of strings separated by spaces
    word_list_with_punctuation = full_text_input.split()
    # Iterates through word_list stripping each word of leading and trailing apostrophes and
    # hyphens and chacking for leading and trialing double quotation marks.
    for word in word_list_with_punctuation:
        if word[-1] == '"':
            end_quotes = True
        if word[0] == '"':
            start_quotes = True
        word = word.strip("'-\"")
        if words(word) != []:
            # Checks if word is end of sentence, if so, turns sentence list into a string, calls
            # the words function, and appends the list of words into a new list of lists of words
            # in each sentence.  Also adds back double quotes if present.
            if word[-1] in (".", "?", "!"):
                if end_quotes and start_quotes:
                    sentence.append('"' + word + '"')
                    end_quotes = False
                    start_quotes = False
                elif start_quotes and not end_quotes:
                    sentence.append('"' + word)
                    start_quotes = False
                elif end_quotes and not start_quotes:
                    sentence.append(word + '"')
                    end_quotes = False
                else:
                    sentence.append(word)
                sentence_string = " ".join(sentence)
                sentences_list_of_word_lists.append(words(sentence_string))
                sentence = []
            elif end_quotes and start_quotes:
                sentence.append('"' + word + '"')
                end_quotes = False
                start_quotes = False
            elif start_quotes and not end_quotes:
                sentence.append('"' + word)
                start_quotes = False
            elif end_quotes and not start_quotes:
                sentence.append(word + '"')
                end_quotes = False
            else:
                sentence.append(word)

    return sentences_list_of_word_lists


def smog_grade(full_text_input):
    """
    Calculates the SMOG grade of the full text by utilizing the words()
    and sentences() functions.
    """
    words_list = words(full_text_input)  # A list of individual words in full_text_input
    num_polysyllables = 0  # Number of words with 3 or more syllables in them
    num_sentences = len(sentences(full_text_input))  # Total # of sentences in full_text_input
    # Checks if the number of sentences in full_text_input is > or = to 30 sentences.
    # If so, it checks each word gainst _syllables dictionary to determine number of syllables.
    # Then proceeds to calculate the SMOG Grade of full_text_input.
    if num_sentences >= 30:
        for word in words_list:
            if len(syllables(word)) >= 3:
                num_polysyllables += 1
        smog_calc = 1.0430 * math.sqrt(num_polysyllables * 30 / num_sentences) + 3.1291
        return smog_calc
    else:
        return None


# Checks to see if file itself is run as a script, if so, prints smog_grade for a given
# standard input.
if __name__ == "__main__":
    print(smog_grade(sys.stdin.read()))
