import re
from typing import List

russian_to_english = {
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P", "С": "C", "Т": "T", "У": "Y", "Х": "X"
}


def replace_russian_letters(text: str) -> str:
    return ''.join(russian_to_english.get(char, char) for char in text)


def get_serial_numbers(text: str) -> List[str]:
    numbers = re.findall(r'[A-Za-zА-Яа-я]+[0-9]{7,}', text)
    return [replace_russian_letters(number.upper()) for number in numbers]


def combine_serial_numbers(theme: str, desc: str) -> List[str]:
    theme_serials = get_serial_numbers(theme)
    desc_serials = get_serial_numbers(desc)

    combined = []
    for serial in theme_serials + desc_serials:
        if serial not in combined:
            combined.append(serial)
    return combined


def to_fixed(numObj: float, digits: int = 0) -> str:
    return f"{numObj:.{digits}f}"
