import re

RE_LETTER = re.compile(r"[a-zA-Z]+")


def fullmatch_regex(word: str, regex=RE_LETTER) -> bool:
    return re.fullmatch(regex, word) is not None
