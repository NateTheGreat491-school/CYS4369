# File:     Decrypt Library
# Dev:      Nathan W. Barors
# Origin:   2026-10-28 11:52:57
# Edited:   2026-10-28 21:09:10

import string
import math

def reverse(string: str, key: None = None) -> str:
    return string[::-1]

def caesar(msg: str, shift: int = 0) -> str:
    shift %= 26

    lowers: str     = string.ascii_lowercase
    uppers: str     = string.ascii_uppercase
    new_lowers: str = lowers[-shift:] + lowers[:-shift]
    new_uppers: str = uppers[-shift:] + uppers[:-shift]

    table: dict = str.maketrans(
        string.ascii_letters, 
        new_lowers + new_uppers
    )

    return msg.translate(table)

def transposition(message, key):
   numOfColumns = int(math.ceil(len(message) / float(key)))
   numOfRows = key
   numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)
   plaintext = [''] * numOfColumns
   column = 0
   row = 0
   for symbol in message:
      plaintext[column] += symbol
      column += 1
      if (column == numOfColumns) or (column == numOfColumns - 1 and
                                row >= numOfRows - numOfShadedBoxes):
         column = 0
         row += 1
   return ''.join(plaintext)
