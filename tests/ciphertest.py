# File:    ciphertest.py
# Devs:    Nathan W. Barros
# Origin:  2026-11-26
# Edited:  2026-11-26

import sys
import time
import string
import random

from typing import Any
from pathlib import Path
from types import ModuleType
from collections.abc import Callable

# ADD SRC PATH FOR THE FOLLOWING IMPORTS
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import encrypt
import decrypt
import util



TOTAL_TESTS: int = 1000
MIN_CHARS: int   = 5
MAX_CHARS: int   = 25
SYMBOLS = string.printable

def _get_callable(name: str, module: ModuleType) -> Callable:
    fptr = getattr(module, name, None)
    if not callable(fptr):
        raise ValueError(f"Cipher [{name}] not found in [{module.__name__}]")
    return fptr

def _show_help() -> None:
    print(f"Usage: python {sys.argv[0]} <cipher_name>")
    sys.exit(1)

def _get_random_cipherkey(name: str, plaintext: str) -> Any:
    match name:
        case "transposition":
            return random.randint(2, max(2, len(plaintext)))

        case _:
            return random.randint(0, int(time.perf_counter()))


# arg0 = cipher name
def main() -> None:
    if len(sys.argv) < 2:
        _show_help()

    cipher_name = sys.argv[1]
    encryptfx = _get_callable(cipher_name, encrypt)
    decryptfx = _get_callable(cipher_name, decrypt)

    test_strings = util.get_random_strlist(MIN_CHARS, MAX_CHARS, TOTAL_TESTS, SYMBOLS)

    successes = 0
    start_time = time.perf_counter()

    print(f"Starting tests for {cipher_name}")
    for iteration, plaintext in enumerate(test_strings, start=1):
        key = _get_random_cipherkey(cipher_name, plaintext)

        ciphertext = encryptfx(plaintext, key)
        recovered  = decryptfx(ciphertext, key)

        if recovered == plaintext:
            successes += 1

        if iteration % 100 == 0:
            elapsed = time.perf_counter() - start_time
            percent = (successes / iteration) * 100
            print(f"[{iteration}/{TOTAL_TESTS}] Success: {percent:.2f}% | Elapsed: {elapsed:.3f}s")

    elapsed = time.perf_counter() - start_time
    success_rate = (successes / TOTAL_TESTS) * 100

    print(f"\n\nFinal Success rate: {success_rate:.2f}% ({successes}/{TOTAL_TESTS}) in {elapsed:.3f}s")

if __name__ == "__main__":
    main()

# EOF
