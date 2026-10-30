# File:     Encrypt Library
# Dev:      Nathan W. Barors
# Origin:   2026-10-28 11:52:57
# Edited:   2026-10-28 11:53:00

import string

def reverse(string: str, key: None = None) -> str:
    return string[::-1]

def caesar(msg: str, shift: int = 0) -> str:
    shift %= 26

    lowers: str     = string.ascii_lowercase
    uppers: str     = string.ascii_uppercase
    new_lowers: str = lowers[shift:] + lowers[:shift]
    new_uppers: str = uppers[shift:] + uppers[:shift]

    table: dict = str.maketrans(
        string.ascii_letters, 
        new_lowers + new_uppers
    )

    return msg.translate(table)

def transposition(message, key):
   ciphertext = [''] * key

   for column in range(key):
      currentIndex = column
      while currentIndex < len(message):
         ciphertext[column] += message[currentIndex]
         currentIndex += key
   return ''.join(ciphertext)

