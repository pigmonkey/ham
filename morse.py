#!/usr/bin/env python2
#
# A Python script which encodes an ASCII message with International Morse Code
# and plays the message with a system beep.
#
# The beeps are played with Johnathan Nightingale's beep. This program must
# be downloaded and compiled by the user.
# http://www.johnath.com/beep/
#
# This script could be used in conjuction with John Walker's codegroup, which
# converts any binary data into five-letter code groups, thereby bypassing
# internet censorship.
# http://www.fourmilab.ch/codegroup/
#
# Author:   Pig Monkey (pm@pig-monkey.com)
# Website:  https://github.com/pigmonkey/ham
#
###############################################################################
import argparse
import os
import subprocess
import sys
import time

# Initialize the needed variables.
# These can be set here, but will be overriden by command-line options.
FILE = None
BEEP = None
SPEED = None
QUIET = False

# The frequency of the beep.
FREQUENCY = 600

# The length of the dit (.) in seconds.
DIT = 0.1

# The length of the dah (-) in seconds.
DAH = DIT * 3

# The length of the pause between beeps, in seconds.
ELEMENT_PAUSE = DIT

# The separator to print between message characters.
CHARACTER_SEPARATOR = ' '

# The length of the pause between message characters, in seconds.
CHARACTER_PAUSE = DIT * 3

# The separator to print between message character groups, such as words.
GROUP_SEPARATOR = '   '

# The length of the pause between message character groups, in seconds.
GROUP_PAUSE = DIT * 7

# End configuration.
###############################################################################

# Set available command-line arguments.
parser = argparse.ArgumentParser(description='Convert an ASCII file to International Morse Code and play it with system beeps.')
parser.add_argument('-b', '--beep', action='store', dest='beep',
                    help="The location of the program that plays the beeps.\
                          This script is intended to be used with Johnathan \
                          Nightingale's beep:\
                          http://www.johnath.com/beep/")
parser.add_argument('-s', '--speed', action='store', dest='speed',
                    help='Reduce the pauses between message characters by the \
                          given amount.')
parser.add_argument('-f', '--file', action='store', dest='file',
                    help='The location of the ASCII file to convert.')
parser.add_argument('-q', '--quiet', action='store_const', const=True,
                    help='Do not print the dots and dashes.')

# Parse command-line arguments.
args = parser.parse_args()
if args.beep:
    BEEP = args.beep
if args.speed:
    try:
        SPEED = float(args.speed)
    except ValueError:
        print 'The speed adjustment number must be a number.'
        sys.exit(1)
if args.file:
    FILE = args.file
if args.quiet:
    QUIET = args.quiet

# If a beep program has been given, make sure that it exists.
if BEEP and not os.path.exists(BEEP):
    print 'Could not find beep at %s.' % BEEP
    sys.exit(1)

# Adjust the length of pauses, if requested.
if SPEED > 0:
    ELEMENT_PAUSE = ELEMENT_PAUSE / SPEED
    CHARACTER_PAUSE = CHARACTER_PAUSE / SPEED
    GROUP_PAUSE = GROUP_PAUSE / SPEED

# If no file was specified, read from standard input.
if FILE is None:
    message = sys.stdin
# If a file was specified, open it.
else:
    try:
        message = open(FILE, 'rb')
    except:
        print 'Could not open file %s.' % FILE
        sys.exit(1)

# Define International Morse Code.
morse = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
         'F': '..-.', 'G': '--.',  'H': '....', 'I': '..',  'J': '.---',
         'K': '-.-',  'L': '.-..', 'M': '--',   'N': '-.',  'O': '---',
         'P': '.--.', 'Q': '--.-', 'R': '.-.',  'S': '...', 'T': '-',
         'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-','Y': '-.--',
         'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
         '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
         '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '.----.',
         "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.',
         ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.',
         '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
         '"': '.-..-.', '$': '...-..-', '@': '.--.-.'}


def beep(length, frequency=FREQUENCY):
    """Use an audio program to play a beep."""
    subprocess.check_call([BEEP, '-l', str(length), '-f', str(frequency)])


def play(morse):
    """Play a morse character and sleep for the proper pause length."""
    for char in morse:
        if char == '.':
            beep(DIT * 1000)
            time.sleep(ELEMENT_PAUSE)
        if char == '-':
            beep(DAH * 1000)
            time.sleep(ELEMENT_PAUSE)
        if char == CHARACTER_SEPARATOR:
            time.sleep(CHARACTER_PAUSE)
        if char == GROUP_SEPARATOR:
            time.sleep(GROUP_PAUSE)


# Encode the message.
for line in message:
    morse_message = []

    for char in line:
        if char == ' ':
            morse_message.append(GROUP_SEPARATOR)
        else:
            if char.upper() in morse:
                morse_message.append(morse[char.upper()])
                morse_message.append(CHARACTER_SEPARATOR)
            else:
                morse_message.append(GROUP_SEPARATOR)

    if not QUIET:
        print ''.join(morse_message)

    if BEEP:
        for char in morse_message:
            play(char)

# Close the file.
message.close()
