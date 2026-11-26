# File:    util.py
# Devs:    Nathan W. Barros
# Origin:  2026-11-17
# Edited:  2026-11-17

import math
import string
import random

DEFAULT_MATRIX_KEY = [
    [ 6, 24,  1],
    [13, 16, 10],
    [20, 17, 15]
]

# GENERAL HELPERS
# ---------------------------------------------
def text_to_numbers(text: str) -> list[int]:
    return [string.ascii_lowercase.index(c) for c in text.lower() if c in string.ascii_lowercase]

def numbers_to_text(nums: list[int]) -> str:
    return "".join(string.ascii_lowercase[n % 26] for n in nums)

def pad_to_block(nums: list[int], block_size: int) -> list[int]:
    pad_len = (-len(nums)) % block_size
    return nums + [string.ascii_lowercase.index('x')] * pad_len

# GENERAL MATH
# ---------------------------------------------
def egcd(a: int, b: int) -> tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def modular_inv(a: int, m: int = 26) -> None|int:
    g, x, _ = egcd(a % m, m)
    if g != 1:
        return None
    return x % m

# MATRIX FUNCTIONS
# ---------------------------------------------
def matrix_mul(A, B, m: int = 26) -> list[list[int]]:
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) % m for j in range(n)] for i in range(n)]


def matrix_add(A, B):
    """Element-wise sum of two matrices of identical shape."""
    if len(A) != len(B) or any(len(r1) != len(r2) for r1, r2 in zip(A, B)):
        raise ValueError("Matrices must have identical dimensions")
    return [[a + b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]


def matrix_sub(A, B):
    """Element-wise difference A − B of two matrices of identical shape."""
    if len(A) != len(B) or any(len(r1) != len(r2) for r1, r2 in zip(A, B)):
        raise ValueError("Matrices must have identical dimensions")
    return [[a - b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]

def matrix_invmod(A: list[list[int]], m: int = 26) -> list[list[int]] | None:
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("Matrix must be square")

    # ---------- Special-case 3×3 via adjugate (recommended for Hill cipher) ----------
    if n == 3:
        a, b, c = A[0]
        d, e, f = A[1]
        g, h, i = A[2]

        # Cofactors
        A11 =  (e * i - f * h)
        A12 = -(d * i - f * g)
        A13 =  (d * h - e * g)
        A21 = -(b * i - c * h)
        A22 =  (a * i - c * g)
        A23 = -(a * h - b * g)
        A31 =  (b * f - c * e)
        A32 = -(a * f - c * d)
        A33 =  (a * e - b * d)

        det = (a * A11 + b * A12 + c * A13) % m
        det_inv = modular_inv(det, m)
        if det_inv is None:
            return None

        # Adjugate = transpose of cofactor matrix
        adj = [
            [A11, A21, A31],
            [A12, A22, A32],
            [A13, A23, A33]
        ]

        return [[(det_inv * adj[r][c]) % m for c in range(3)] for r in range(3)]

def matrix_mod(A, m: int = 26) -> list[list[int]]:
    return [[x % m for x in row] for row in A]

def matrix_vec_mul(A, vec: list[int], m: int = 26) -> list[list[int]]:
    n = len(A)
    return [sum(A[i][k] * vec[k] for k in range(n)) % m for i in range(n)]

def matrix_equal(A, B) -> bool:
    if len(A) != len(B):
        return False
    return all(len(rowA) == len(rowB) and rowA == rowB for rowA, rowB in zip(A, B))

# RANDOM TEXT GENERATION FOR TESTING
# ---------------------------------------------
def get_random_string(min_length: int, max_length: int, symbols: str) -> str:
    if min_length > max_length:
        raise ValueError("min_length must be less than max_length")
    elif min_length < 0:
        raise ValueError("min_length must be greater than 0")
    if not symbols:
        raise ValueError("Symbols must not be empty")

    random_length = random.randint(min_length, max_length)
    return "".join( random.choices(symbols, k=random_length) )

def get_random_strlist(min_length: int, max_length: int, count: int, symbols: str) -> list[str]:
    if count < 0:
        raise ValueError("Count must be non-negative")

    return [
        get_random_string(min_length, max_length, symbols)
        for _ in range(count)
    ]

# EOF
