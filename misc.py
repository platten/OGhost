"""misc.py: Optimal Ghost auxiliary functions."""

__author__      = "Paul Pietkiewicz"
__copyright__   = "Copyright 2012, Paul Pietkiewicz"
__license__     = "GPL"
__version__     = "0.1"
__email__       = "paul.pietkiewicz@acm.org"


from trie import Trie, IncompleteWord, flatten
from random import choice
from string import ascii_letters

WORDLIST_URL = 'http://itasoftware.com/careers/work-at-ita/PuzzleFiles/WORD.LST'


class LostException(Exception):
    pass


def print_greeting():
    """Print greeting"""
    print "hello"


def download_wordlist():
    """Download wordlist"""
    from urllib2 import urlopen

    response = urlopen(WORDLIST_URL)
    with open('WORD.LST', 'w') as fp:
        fp.write(response.read())


def create_data_structure(filepath):
    """Open file and load wordlist into Trie ds"""
    ds = Trie()
    with open(filepath, 'r') as fp:
        for word in fp:
            ds.add_word(word.rstrip())
    return ds


def computer_turn(ds, letter_list):
    """Play AI turn"""
    word = "".join(letter_list)
    height_dict = ds.get_max_child_height_dict(word)
    if letter_list > 4:
        # Look at the remaining word length and choose letters which have an
        # even path length (forcing the user to complete the word)
        winning_list = flatten([height_dict[i] for i in height_dict.keys()
                                if i % 2 == 0])
        if winning_list:
            move = choice(winning_list)
        else:
            # When the AI is loosing, try to prolong the game as long as
            # possible, and hope the player makes a mistake
            move = choice(height_dict[max(height_dict.keys())])
            try:
                word = ds[word + move]
                msg = "%s is a word. Player wins!" % word
                raise LostException(msg)
            except IncompleteWord:
                return move
    else:
        # make sure chosen word has 4 characters or longer
        possibilities = flatten([height_dict[i] for i in height_dict.keys()
                                 if (i + len(letter_list)) >= 4])
        move = choice(possibilities)
    return move


def player_turn(ds, letter_list):
    """Play player turn"""
    letter = get_letter()
    proposed_word_prefix = "".join(letter_list) + letter

    try:
        word = ds[proposed_word_prefix]
        if word and len(letter_list) > 3:
            msg = "%s is a word. Player lost!" % word
            raise LostException(msg)
    except KeyError:
        msg = "No words exist in wordlist beginning with %s. Player lost! " %\
               proposed_word_prefix
        raise LostException(msg)
    except IncompleteWord:
        return letter
    return letter

def get_letter():
    """Get a single letter from the player"""
    letter = raw_input("Provide a letter: ").lower()
    while len(letter) > 1 and letter not in ascii_letters:
        print "ERROR: provide a single letter between a to z"
        letter = raw_input("Provide a letter: ").lower()
    return letter
