# File:     Hack
# Devs:     Nathan W. Barros
# Origin:   2026-10-28 22:04:50
# Edited:   2026-10-28 22:04:54

from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0
COMMON_WORDS = {"the", "be", "to", "of", "and", "a", "in", 
                "that", "have", "i", "it", "for", "not", "on", 
                "with", "he", "she", "am", "I", "who", "what",
                "when", "where", "why"}

def is_english(text: str) -> bool:
    try:
        
        if detect(text) != "en": return False

        words   = set(text.lower().split())
        matches = words.intersection(COMMON_WORDS)

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
