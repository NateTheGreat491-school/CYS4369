# File:     Hack
# Devs:     Nathan W. Barros
# Origin:   2026-10-28 22:04:50
# Edited:   2026-10-28 22:04:54

from langdetect import detect, DetectorFactory
import math

DetectorFactory.seed = 0
COMMON_WORDS = {"the", "be", "to", "of", "and", "a", "in", 
                "that", "have", "i", "it", "for", "not", "on", 
                "with", "he", "she", "am", "I", "who", "what",
                "when", "where", "why"}

EN_LETTER_FREQ = list(x for x in "etaonrishdlfcmugypwbvkjxzq");
EN_PAIR_LETTER_FREQ = list("th he an re er in on at nd st es en of te ed or ti hi as to".split(" "))
EN_DOUBLE_LETTER_FREQ = list("ll ee ss oo tt ff rr nn pp cc".split(" "))

def is_english(text: str) -> bool:
    try:
        
        if detect(text) != "en": return False

        words   = set(text.lower().split())
        if not words:
            return False

        matches = words.intersection(COMMON_WORDS)

        if len(words) <= 2:
            return True
        if len(words) <= 4:
            return len(matches) >= 1
        return len(matches) >= 2

    except Exception:
        return False

def caesar(msg: str, shift: int = 0) -> str:
    """ Brute force caesar cipher attack """

    for key in range(26):
        decrypted_msg = []

        for char in msg:
            if char.isalpha():
                offset = ord('A') if char.isupper() else ord('a')
                origin = (ord(char) - offset - key) % 26
                decrypted_msg.append(chr(origin + offset))
            else:
                decrypted_msg.append(char)

        decrypted_msg = "".join(decrypted_msg)

        # Check if the decrypted result is valid English
        if is_english(decrypted_msg):
            return f"KEY: {key}\n\n{decrypted_msg}"

    return "Failed to find suitable English translation of this cipher."

def transposition(msg: str, key: int) -> str:
    """ Brute force transposition hack """

    # get total length of msg
    # count all the letters present in msg & frequency
    # include double letters and pair letters
    # try to decode using all of that inforamtion
    
    normal: dict = dict(zip(EN_LETTER_FREQ, 0))

    for c in msg:
        normal[c] += 1

    return msg

def affine(msg: str, a: int, b: int, m: int = 26) -> str:
    """ Brute force affine cipher hack """

    possible_a = [a for a in range(1, 26) if math.gcd(a, 26) == 1] 
    
    results = []
    for a in possible_a:
        a_inv = pow(a, -1, 26)
        
        for b in range(26):
            result = []
                
            for c in msg:
                if c.isalpha():
                    offset = ord('A') if c.isupper() else ord('a')
                    x = ord(c) - offset
                    y = (a_inv * (x-b)) % 26
                    result.append(chr(y + offset))
                else:
                    result.append(c)

            canidate = ''.join(result)
            results.append(canidate)
            if is_english(canidate):
                return f"KEY: a={a}, b={b}\n\n{canidate}"
        
    return "Failed to find suitable english translation of this cipher.\n\n" + '\n'.join(results)

