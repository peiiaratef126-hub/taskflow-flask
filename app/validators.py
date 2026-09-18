import re

# Physical keyboard layouts for adjacency detection
QWERTY_COORDS = {
    'q': (0,0), 'w': (0,1), 'e': (0,2), 'r': (0,3), 't': (0,4), 'y': (0,5), 'u': (0,6), 'i': (0,7), 'o': (0,8), 'p': (0,9),
    'a': (1,0), 's': (1,1), 'd': (1,2), 'f': (1,3), 'g': (1,4), 'h': (1,5), 'j': (1,6), 'k': (1,7), 'l': (1,8),
    'z': (2,0), 'x': (2,1), 'c': (2,2), 'v': (2,3), 'b': (2,4), 'n': (2,5), 'm': (2,6)
}

ARABIC_COORDS = {
    'ض': (0,0), 'ص': (0,1), 'ث': (0,2), 'ق': (0,3), 'ف': (0,4), 'غ': (0,5), 'ع': (0,6), 'ه': (0,7), 'خ': (0,8), 'ح': (0,9), 'ج': (0,10), 'د': (0,11),
    'ش': (1,0), 'س': (1,1), 'ي': (1,2), 'ب': (1,3), 'ل': (1,4), 'ا': (1,5), 'أ': (1,5), 'إ': (1,5), 'آ': (1,5), 'ت': (1,6), 'ن': (1,7), 'م': (1,8), 'ك': (1,9), 'ط': (1,10),
    'ئ': (2,0), 'ء': (2,1), 'ؤ': (2,2), 'ر': (2,3), 'ى': (2,4), 'ة': (2,5), 'و': (2,6), 'ز': (2,7), 'ظ': (2,8)
}

COMMON_MASH_SUBSTRINGS = [
    # English patterns
    "asd", "lkj", "jkl", "qwe", "zxc", "poi", "mnb", "dfg", "ghj",
    # Arabic patterns
    "شسي", "شس", "سش", "يبل", "بلات", "تنتن", "نتنت", "ضصث", "صثق", "ثقف", "قفغ", "كمن"
]

def calculate_adjacency_ratio(word: str, coords_map: dict) -> float:
    """Calculates the ratio of transitions between physically adjacent keys."""
    chars = [c.lower() for c in word if c.lower() in coords_map]
    if len(chars) < 4:
        return 0.0
    adjacent_count = 0
    total_transitions = len(chars) - 1
    for i in range(total_transitions):
        r1, c1 = coords_map[chars[i]]
        r2, c2 = coords_map[chars[i+1]]
        # Adjacent if within 1 step on row and column
        if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
            adjacent_count += 1
    return adjacent_count / total_transitions

def is_meaningful_text(text: str) -> tuple[bool, str]:
    cleaned = text.strip()

    # 1. Length constraint
    if len(cleaned) < 3 or len(cleaned) > 120:
        return False, "يجب أن يتراوح طول المهمة بين 3 و 120 حرفاً."

    # 2. Must contain at least one letter (Arabic or English)
    if not any(c.isalpha() for c in cleaned):
        return False, "يرجى إدخال نص مهمة صالح يحتوي على أحرف واضحة."

    # 3. Reject identical repeated characters (e.g., 'aaaa', 'تتتت')
    if re.search(r'(.)\1{2,}', cleaned):
        return False, "النص يحتوي على أحرف مكررة بشكل غير طبيعي."

    # 4. Reject oscillating 2-3 char patterns (e.g. 'تنتنتن', 'asdasd', 'تنتننت')
    if re.search(r'(.{2,3})\1{1,}', cleaned) and len(cleaned) <= 10:
        return False, "النص يبدو كضغط متكرر على لوحة المفاتيح."

    # 5. Check known keyboard mash sequences (e.g. 'lkjasd', 'تنتننتسي')
    lower_text = cleaned.lower()
    for pattern in COMMON_MASH_SUBSTRINGS:
        if pattern in lower_text:
            return False, "النص المدخل يبدو كضغط عشوائي على لوحة المفاتيح."

    # 6. Analyze words individually
    words = cleaned.split()
    for word in words:
        clean_word = "".join(c for c in word if c.isalpha())
        if len(clean_word) >= 5:
            # Low character variety check (e.g. 4 unique chars in 8 letters)
            if len(set(clean_word.lower())) / len(clean_word) < 0.5:
                return False, "النص يفتقر للتنوع الطبيعي في الحروف."

            # English word checks
            if all('a' <= c <= 'z' for c in clean_word.lower()):
                # Must contain at least one vowel
                if not any(c in "aeiouy" for c in clean_word.lower()):
                    return False, "الكلمات الإنجليزية يجب أن تحتوي على حروف علة مقروءة."
                # 4+ consecutive consonants
                if re.search(r'[bcdfghjklmnpqrstvwxyz]{4,}', clean_word.lower()):
                    return False, "الكلمة تحتوي على تتابع غير طبيعي لحروف ساكنة."
                # Physical keyboard adjacency ratio (e.g. 'lkjasd')
                if calculate_adjacency_ratio(clean_word, QWERTY_COORDS) >= 0.65:
                    return False, "النص يبدو كضغط عشوائي على الكيبورد الإنجليزي."

            # Arabic word physical adjacency check (e.g. 'تنتننتسي')
            if any('\u0600' <= c <= '\u06FF' for c in clean_word):
                if calculate_adjacency_ratio(clean_word, ARABIC_COORDS) >= 0.65:
                    return False, "النص يبدو كضغط عشوائي على الكيبورد العربي."

    return True, ""
