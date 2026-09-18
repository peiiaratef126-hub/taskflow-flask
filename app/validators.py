import re

# Standard Arabic physical keyboard layout (Rows 0, 1, 2)
ARABIC_KEYBOARD_ROWS = [
    "ضصثقفغعهخحجدذ",   # Top row
    "شسيبلاتنمكط",     # Home row
    "ئءؤرىةوزظ",       # Bottom row
]

# Incompatible Arabic consonant pairs (letters that cannot co-occur adjacently in Arabic stems)
INCOMPATIBLE_ARABIC_PAIRS = [
    "شس", "سش",
    "صس", "سص",
    "صش", "شص",
    "ضظ", "ظض",
    "عغ", "غع",
    "حخ", "خح",
    "ثظ", "ظث",
    "ثص", "صث",
    "ثس", "سث",
    "ظز", "زظ",
    "ذز", "زذ",
    "قك", "كق",
    "جق", "قج",
]

KEYBOARD_RUNS = [
    # English keyboard patterns
    "asdfg",
    "qwerty",
    "zxcvb",
    "poiuy",
    "lkjhg",
    # Arabic keyboard patterns (runs along rows)
    "ضصثق",
    "صثقف",
    "ثقفغ",
    "شسيبل",
    "شسيب",
    "سيبل",
    "تنمكط",
    "نمكط",
    "كمنتال",
    "طكمنت",
    "بيسش",
    "لبيسش",
    "ئءؤر",
    "ءؤرى",
    "ةوزظ",
    "ظزوة",
]

VOWELS = set("aeiouy")
CONSONANT_CLUSTER_REGEX = re.compile(r"[bcdfghjklmnpqrstvwxz]{5,}", re.IGNORECASE)
REPEATED_CHARS_REGEX = re.compile(r"(.)\1{2,}")


def is_meaningful_text(text: str) -> tuple[bool, str]:
    """Validate that text is meaningful and readable, rejecting keyboard mash and gibberish.

    Supports both English and Arabic language heuristics (phonotactics & keyboard layout).

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

    # 3. Arabic Phonotactic Incompatibility & Mash Detection
    for pair in INCOMPATIBLE_ARABIC_PAIRS:
        if pair in text:
            return False, "النص يبدو كضغط عشوائي على لوحة المفاتيح."

    # 4. Vowel & Consonant Check (for Latin/English Words)
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

    # 5. Entropy / Variety Check (for words longer than 5 letters)
    # Ensure at least 3 unique characters exist (blocks ababab, etc.)
    words = re.findall(r"\w+", text)
    for word in words:
        if len(word) > 5:
            unique_chars = set(word.lower())
            if len(unique_chars) < 3:
                return False, "يرجى كتابة نص ذي معنى."

    return True, ""
