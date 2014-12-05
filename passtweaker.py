#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
#
# Password Tweaker
# Transforms password lists in list of passwords
# that would meet the Windows 7/2008 complexity requirements

import argparse
import re
import traceback

def parse_words(words_file):

    # Read the wordlist
    with open(words_file, 'r') as file:
        lines = [line.rstrip() for line in file]

    # Loop through the words
    for word in lines:

        # Initial Form
        if args.debug:
            print "FROM: %s" % word

        # Check if it matches the requirements
        if tryAppend(word):
            continue

        # Upper First Char
        uFirst = word[0].upper()
        word = uFirst + word[1:]

         # Check if it matches the requirements
        if tryAppend(word):
            continue

        # Fill up the space with numbers or special chars
        num_chars = len(word)
        if num_chars < 7:
            new_word = fill_up_inc(word)
            tryAppend(new_word)
            new_word = fill_up_dec(word)
            tryAppend(new_word)

        # Fill up with single char
        if num_chars == 7:
            new_word = word + "!"
            tryAppend(new_word)
            new_word = word + "$"
            tryAppend(new_word)
            new_word = word + "%"
            tryAppend(new_word)
            new_word = word + "?"
            tryAppend(new_word)
            new_word = word + "1"
            tryAppend(new_word)

        # If 8 characters used try to replace chars with numbers
        if num_chars == 8:
            for new_word in replace_chars(word):
                tryAppend(new_word)

def tryAppend(word):
    if meets_requirements(word):

        # Normal mode
        if not args.intense:
            complex_words.append(word)
            return 1

        # Intense mode
        else:
            for new_word in replace_chars(word):
                append_word(new_word)
            return 1

    return 0

def append_word(word):
    if not word in complex_words:
        complex_words.append(word)

def fill_up_inc(word):
    i = 1
    while len(word) < 8:
        word = word + str(i)
        i += 1
    return word

def fill_up_dec(word):
    i = 9
    while len(word) < 8:
        word = word + str(i)
        i -= 1
    return word

def replace_chars(word):
    yield word.replace("a", "@", 1)
    yield word.replace("a", "@")
    yield word.replace("o", "0", 1)
    yield word.replace("o", "0").replace("a", "@")
    yield word.replace("e", "3", 1)
    yield word.replace("e", "3")
    yield word.replace("s", "5", 1)
    yield word.replace("s", "5")
    yield word.replace("i", "1", 1)
    yield word.replace("i", "1")

def meets_requirements(word):

    # 8 chars
    if len(word) < 8:
        return 0
    # Upper Case Char
    if not re.search(r'[A-Z]', word):
        return 0
    # Upper Case Char
    if not re.search(r'[a-z]', word):
        return 0
    # Upper Case Char
    if not re.search(r'[0-9\W]', word):
        return 0

    if args.debug:
     print "TO: %s" % word

    # Contains all necessary chars
    return 1

def printWelcome():
    print "###############################################################################"
    print "  "
    print "  PASSTWEAKER"
    print "  "
    print "  by Florian Roth"
    print "  December 2014"
    print "  Version 0.1"
    print " "
    print "###############################################################################"

# MAIN ################################################################
if __name__ == '__main__':

    # Parse Arguments
    parser = argparse.ArgumentParser(description='PassTweaker')
    parser.add_argument('-f', help='File to transform')
    parser.add_argument('-o', help='Output file', default="complex-pass.txt")
    parser.add_argument('--intense', action='store_true', default=False, help='Try even to improve words that already match the requirements')
    parser.add_argument('--debug', action='store_true', default=False, help='Debug output')

    args = parser.parse_args()

    # Print Welcome
    printWelcome()

    global complex_words
    complex_words = []
    # Parse words
    parse_words(args.f)

    if args.debug:
        print complex_words

    # Write complex words
    outfile = open(args.o, "w")
    outfile.write("\n".join(complex_words))
    outfile.close()