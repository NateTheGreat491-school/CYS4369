# File:     Encrypt Library
# Dev:      Nathan W. Barors
# Origin:   2026-10-28 11:52:57
# Edited:   2026-10-28 11:53:00

import string
import math
import secrets
import util

def reverse(string: str, key: None = None) -> str:
    return string[::-1]

def caesar(msg: str, shift: int = 0) -> str:
    shift %= 26

    lowers: str     = string.ascii_lowercase
    uppers: str     = string.ascii_uppercase
    new_lowers: str = lowers[shift:] + lowers[:shift]
    new_uppers: str = uppers[shift:] + uppers[:shift]

    table: dict = str.maketrans(
        string.ascii_letters, new_lowers + new_uppers
    )

    return msg.translate(table)

def transposition(msg: str, key: int) -> str:
    if not msg or key <= 1:
        return msg

    return ''.join(msg[i::key] for i in range(key))

def affine(msg: str, a: int, b: int,  m: int = 26) -> str:
    result = []
    for c in msg:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            x = ord(c) - base
            y = (a * x + b) % m
            result.append(chr(y + base))
        else:
            result.append(c)

    return ''.join(result)

def substitution(msg: str, key: int) -> str:
    SYMBOLS = 'abcdefghijklmnopqrstuvwxyz'

    cipherText = ''

    for symbol in msg:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)
            cipherText = cipherText + key[symbolIndex]
        else:
            cipherText = cipherText + symbol

    return cipherText


def OneTimePad(msg: str, k: str) -> str:
    # Set Up Variables
    plainText = msg.upper()
    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = ''
    keyPos = 0  # position in the key that will be analyzed
    cipherText = ''  # cipher text initialized
    # Encrypt
    numPlain = len(plainText)
    for i in range(numPlain):
        key += secrets.choice(SYMBOLS)

    numKey = len(key)  # length of key
    numSym = len(SYMBOLS)  # number of recognized symbols

    for symbol in plainText:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)  # where is the current plain text character?
            keyIndex = SYMBOLS.find(key[keyPos])  # where is the current key character?
            cipherIndex = symbolIndex + keyIndex  # compute cipher Index
            cipherIndex = cipherIndex % numSym
            cipherText = cipherText + SYMBOLS[cipherIndex]
        else:
            cipherText = cipherText + symbol  # no change if not in symbols
        keyPos += 1  # increment key
        keyPos = keyPos % numKey
    key = "\nKey: " + key
    cipherText = cipherText + key
    return cipherText

def matrix(msg: str, key: list[list[int]]) -> str:
    if key is None:
        key = DEFAULT_MATRIX_KEY
    key = util.matrix_mod(key)
    n = len(key)

    if any(len(row) != n for row in key):
        raise ValueError("Key must be a square matrix")

    nums = util.pad_to_block(util.text_to_numbers(msg), n)
    ciphertext = []
    for i in range(0, len(nums), n):
        block = nums[i:i + n]
        ciphertext.extend(util.matrix_vec_mul(key, block))
    return util.numbers_to_text(ciphertext)
