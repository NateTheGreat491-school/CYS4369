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

def substitution(msg: str, key: int) -> str:
    SYMBOLS = 'abcdefghijklmnopqrstuvwxyz'
    plainText = ''

    for symbol in msg:
        if symbol in key:
            symbolIndex = key.find(symbol)
            plainText = plainText + SYMBOLS[symbolIndex]
        else:
            plainText = plainText + symbol

    return plainText




