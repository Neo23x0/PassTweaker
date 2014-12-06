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

    print "Reading wordlist '%s' ... " % words_file

    try:
        # Read the wordlist
        with open(words_file, 'r') as file:
            lines = [line.rstrip() for line in file]

        print "Read wordlist '%s' with %s words." % ( words_file, len(lines) )

        if args.debug:
            print "BEFORE"
            print lines

    except:
        traceback.print_exc()

    # Loop through the words
    for word in lines:

        # Initial Form
        #if args.debug:
        #    print "FROM: %s" % word

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
            for new_word in add_special_chars(word):
                tryAppend(new_word)

        # If 8 characters used try to replace chars with numbers
        if num_chars == 8:
            for new_word in replace_chars(word):
                tryAppend(new_word)

            if args.intense:
                # Remove one char and add a special character
                for new_word in add_special_chars(word[:7]):
                    tryAppend(new_word)

        # Append year numbers and special chars
        if args.intense:
            # If word has 4 or 6 chars try to append a year
            if num_chars == 6:
                for new_word in (add_year_numbers(word, chars=2)):
                    tryAppend(new_word)
            if num_chars == 4:
                for new_word in (add_year_numbers(word, chars=4)):
                    tryAppend(new_word)

             # If word has 3 or 5 chars try to append a year and special character
            if num_chars == 5:
                for new_word in (add_year_numbers(word, chars=2)):
                    for newer_word in (add_special_chars(new_word)):
                        tryAppend(newer_word)
            if num_chars == 3:
                for new_word in (add_year_numbers(word, chars=4)):
                    for newer_word in (add_special_chars(new_word)):
                        tryAppend(newer_word)

        # If word is longer than 8 chars - cut it and add 1-2 extra chars


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


def add_special_chars(word):

    special_chars = ['!', '$', '$', '?', '+', '!', '%']

    for char in special_chars:
        yield word + char

def add_year_numbers(word, chars=2):

    startYear = 1970

    if chars == 2:
        startYearShort = int(str(startYear)[-2:])
        for year in (range(startYearShort,99)):
            yield(word+str(year))
        for year in range(0,15):
            if len(str(year)) == 1:
                yield(word + "0" + str(year))
            else:
                yield(word + str(year))

    if chars == 4:
        for year in (range(startYear,2015)):
            yield(word+str(year))


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

    #if args.debug:
        #print "TO: %s" % word

    # Contains all necessary chars
    return 1

def printWelcome():
    print "###############################################################################"
    print "  "
    print "  PASSTWEAKER"
    print "  "
    print "  by Florian Roth"
    print "  December 2014"
    print "  Version 0.2"
    print " "
    print "###############################################################################"

# MAIN ################################################################
if __name__ == '__main__':

    # Parse Arguments
    parser = argparse.ArgumentParser(description='PassTweaker')
    parser.add_argument('-f', metavar="wordlist", help='File to transform', required=True)
    parser.add_argument('-o', metavar="new-wordlist", help='Output file', default="complex-pass.txt")
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
        print "AFTER"
        print complex_words

    # Write complex words
    try:
        outfile = open(args.o, "w")
        outfile.write("\n".join(complex_words))
        outfile.close()

        print "%s words written to improved wordlist '%s'." % ( len(complex_words), args.o)

    except:
        traceback.print_exc()