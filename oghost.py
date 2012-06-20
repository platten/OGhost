#!/usr/bin/env python

"""oghost.py: Optimal Ghost main driver."""

__author__      = "Paul Pietkiewicz"
__copyright__   = "Copyright 2012, Paul Pietkiewicz"
__license__     = "GPL"
__version__     = "0.1"
__email__       = "paul.pietkiewicz@acm.org"


from misc import *
from sys import exit
from os.path import exists

import argparse


def main():
    letter_list = []
    parser = argparse.ArgumentParser(description='Optimal Ghost')
    parser.add_argument('wordlist', metavar='wordlist', default='WORD.LST',
                        nargs='?', help='the wordlist to use')
    args = parser.parse_args()

    if not exists(args.wordlist) and args.wordlist is 'WORD.LST':
        print "Downloading wordlist from itasoftware.com..."
        try:
            download_wordlist()
        except KeyboardInterrupt:
            print '\nKeyboard interrupt detected, exiting...'
            exit(2)
        except:
            print "Could not download wordlist, exiting..."
            exit(1)
    elif not exists(args.wordlist) and args.wordlist is not 'WORD.LST':
        print "Wordlist '%s' does not exist. Exiting..." % args.wordlist
        exit(3)

    print "Loading wordlist: %s" % args.wordlist
    try:
        ds = create_data_structure(args.wordlist)
    except KeyboardInterrupt:
        print '\nKeyboard interrupt detected, exiting...'
        exit(2)
    print "Wordlist loaded.\n"

    try:
        while(True):
            letter_list.append(player_turn(ds, letter_list))
            print "PLAYER:>>   " + "".join(letter_list)
            letter_list.append(computer_turn(ds, letter_list))
            print "COMPUTER:>> " + "".join(letter_list)

    except LostException as e:
        print e.message

    except KeyboardInterrupt:
        print '\nKeyboard interrupt detected, exiting...'
        exit(2)


if __name__ == '__main__':
    main()
    exit(0)
