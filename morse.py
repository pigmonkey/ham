#!/usr/bin/env python
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
import getopt
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

def usage():
    print '''Convert an ASCII file to International Morse Code and play it with system beeps.

    Options:
        -b, --beep BEEP         # The location of the program that plays the beeps.
                                # This script is intended to be used with Johnathan Nightingale's beep:
                                # http://www.johnath.com/beep/
        -q, --quiet             # Don't print dots and dashes.
        -s, --speed SPEED       # Speed up the playback by reducing the pauses between message characters by the given amount.
                                # A number less than 1 will result in slowing down the playback.
        -f, --file FILE         # The location of the ASCII file to convert.
        -h, --help              # Displays this help list.
    '''

# Get any options from the user.
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:qs:f:h",
        ["beep=", "quiet", "speed=" "file=", "help"])
except getopt.GetoptError:
    usage()
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ("-b", "--beep"):
        BEEP = arg
    elif opt in ("-q", "--quiet"):
        QUIET = True
    elif opt in ("-s", "--speed"):
        try:
            SPEED = float(arg)
        except ValueError:
            print 'The speed adjustment number must be a number.'
            sys.exit(1)
    elif opt in ("-f", "--file"):
        FILE = arg

# If a beep program has been given, make sure that it exists.
if BEEP and not os.path.exists(BEEP):
    print 'Could not find beep at %s.' % BEEP
    sys.exit(1)

# Adjust the length of pauses, if requested.
if SPEED > 0:
    ELEMENT_PAUSE = ELEMENT_PAUSE / SPEED
    CHARACTER_PAUSE = CHARACTER_PAUSE / SPEED
    GROUP_PAUSE = GROUP_PAUSE / SPEED

# Check to make sure that a file has been given.
if FILE is None:
    usage()
    sys.exit(1)
else:
    # Make sure that the file can be opened.
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
