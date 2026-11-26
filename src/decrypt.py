# File:     Decrypt Library
# Dev:      Nathan W. Barors
# Origin:   2026-10-28 11:52:57
# Edited:   2026-10-28 21:09:10

import string
import math
import util

from encrypt import matrix as encrypt_matrix

def reverse(string: str, key: None = None) -> str:
    return string[::-1]

def caesar(msg: str, shift: int = 0) -> str:
    shift %= 26

    lowers: str     = string.ascii_lowercase
    uppers: str     = string.ascii_uppercase
    new_lowers: str = lowers[-shift:] + lowers[:-shift]
    new_uppers: str = uppers[-shift:] + uppers[:-shift]

    table: dict = str.maketrans(
        string.ascii_letters, new_lowers + new_uppers
    )

    return msg.translate(table)

def transposition(msg: str, key: int) -> str:
    if not msg or key <= 1:
        return msg

    msg_len: int     = len(msg)
    num_columns: int = math.ceil(msg_len / key)
    num_shaded: int  = (num_columns * key) - msg_len
    full_rows: int   = key - num_shaded

    rows = []
    idx  = 0

    for _ in range(full_rows):
        rows.append(msg[idx : idx + num_columns])
        idx += num_columns

    for _ in range(num_shaded):
        rows.append(msg[idx : idx + num_columns-1])
        idx += num_columns-1

    columns = [
        ''.join(row[c] for row in rows if c < len(row))
        for c in range(num_columns)
    ]

    return ''.join(columns)

def affine(msg: str, a: int, b: int, m: int = 26) -> str:
    a_inv = pow(a, -1, m)
    result = []

    for c in msg:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            x = ord(c) - base
            y = (a_inv * (x - b)) % m
            result.append(chr(y + base))
        else:
            result.append(c)
    return ''.join(result)

def substitution(msg: str, key: str) -> str:
    SYMBOLS = 'abcdefghijklmnopqrstuvwxyz'
    plainText = ''

    for symbol in msg:
        if symbol in key:
            symbolIndex = key.find(symbol)
            plainText = plainText + SYMBOLS[symbolIndex]
        else:
            plainText = plainText + symbol

    return plainText

def OneTimePad(msg: str, key: str) -> str:
    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Get PlainText and Key
    cipherText = msg.upper()
    numCipher = len(cipherText)
    key = key.upper()

    # Set Up Variables
    keyPos = 0  # position in the key that will be analyzed
    numKey = len(key)  # length of key
    numSym = len(SYMBOLS)  # number of recognized symbols
    plainText = ''  # plain text initialized

    # Decrypt
    for symbol in cipherText:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)  # where is the current plain text character?
            keyIndex = SYMBOLS.find(key[keyPos])  # where is the current key character?
            plainIndex = symbolIndex - keyIndex  # compute cipher Index
            plainIndex = plainIndex % numSym
            plainText = plainText + SYMBOLS[plainIndex]
        else:
            plainText = plainText + symbol  # no change if not in symbols
        keyPos += 1  # increment key
        keyPos = keyPos % numKey

    return plainText

def matrix(msg: str, key: list[list[int]] = util.DEFAULT_MATRIX_KEY) -> str:
    inv_key = util.matrix_invmod(key)
    if inv_key is None:
        raise ValueError("Key matrix is not invertible mod 26!")
    return encrypt_matrix(msg, inv_key)

# EOF
def DIY (msg: str, key: int) -> str:

    key2 = 'xmgtaqhbzjwyrcnvksfeupodil'
    SYMBOLS = 'abcdefghijklmnopqrstuvwxyz'
    plainText = ''

    for symbol in msg:
        if symbol in key2:
            symbolIndex = key2.find(symbol)
            plainText = plainText + SYMBOLS[symbolIndex]
        else:
            plainText = plainText + symbol

    msg = plainText.lower()

    if not msg or key <= 1:
        return msg

    # determine how many chars each slice got
    lengths = [len(msg[i::key]) for i in range(key)]

    slices = []
    start = 0

    for length in lengths:
        slices.append(msg[start:start+length])
        start += length

    plaintext = []

    max_len = max(lengths)

    for i in range(max_len):
        for k in range(key):
            if i < len(slices[k]):
                plaintext.append(slices[k][i])

    return ''.join(plaintext)




