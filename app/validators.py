import re

KEYBOARD_RUNS = [
    # English keyboard patterns
    "asdfg",
    "qwerty",
    "zxcvb",
    "poiuy",
    "lkjhg",
    # Arabic keyboard patterns
    "ضصثقف",
    "شسيبل",
    "ئءؤرلا",
    "كمنتال",
]

VOWELS = set("aeiouy")
CONSONANT_CLUSTER_REGEX = re.compile(r"[bcdfghjklmnpqrstvwxz]{5,}", re.IGNORECASE)
REPEATED_CHARS_REGEX = re.compile(r"(.)\1{2,}")


def is_meaningful_text(text: str) -> tuple[bool, str]:
    """Validate that text is meaningful and readable, rejecting keyboard mash and gibberish.

    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not text:
        return False, "النص لا يمكن أن يكون فارغاً."

    # 1. Character Repetition Check (3 or more identical consecutive characters)
    if REPEATED_CHARS_REGEX.search(text):
        return False, "النص يحتوي على أحرف مكررة بشكل غير طبيعي."

    # 2. Keyboard Pattern Check (continuous keyboard runs)
    lower_text = text.lower()
    for pattern in KEYBOARD_RUNS:
        if pattern in lower_text:
            return False, "النص يبدو كضغط عشوائي على لوحة المفاتيح."

    # 3. Vowel & Consonant Check (for Latin/English Words)
    # Checks each alphabetic English word of 4 or more letters
    latin_words = re.findall(r"[a-zA-Z]+", text)
    for word in latin_words:
        if len(word) >= 4:
            # Must contain at least one vowel
            if not any(char.lower() in VOWELS for char in word):
                return False, "يرجى إدخال كلمات واضحة ومقروءة."
            # Must not contain 5 or more consecutive consonants
            if CONSONANT_CLUSTER_REGEX.search(word):
                return False, "يرجى إدخال كلمات واضحة ومقروءة."

    # 4. Entropy / Variety Check (for words longer than 5 letters)
    # Ensure at least 3 unique characters exist (blocks ababab, etc.)
    words = re.findall(r"\w+", text)
    for word in words:
        if len(word) > 5:
            unique_chars = set(word.lower())
            if len(unique_chars) < 3:
                return False, "يرجى كتابة نص ذي معنى."

    return True, ""
