# Source: https://fr.wikipedia.org/wiki/Fr%C3%A9quence_d'apparition_des_lettres_en_fran%C3%A7ais
import operator

LETTER_FREQUENCIES_FR = {
    "a": 0.0746,
    "b": 0.0114,
    "c": 0.0324,
    "d": 0.0367,
    "e": 0.1436,
    "f": 0.0111,
    "g": 0.0123,
    "h": 0.0111,
    "i": 0.0664,
    "j": 0.0034,
    "k": 0.0029,
    "l": 0.0496,
    "m": 0.0262,
    "n": 0.0639,
    "o": 0.0507,
    "p": 0.0249,
    "q": 0.0065,
    "r": 0.0607,
    "s": 0.0651,
    "t": 0.0592,
    "u": 0.0454,
    "v": 0.0111,
    "w": 0.0017,
    "x": 0.0038,
    "y": 0.0046,
    "z": 0.0015,
}


def most_common_letters(candidates: list) -> list[str]:
    """Assign a letter-frequency score to each candidate, then rank them by this score.

    >>> most_common_letters(["bulldog", "biofilm", "bigoudi"])
    ["bigoudi", "biofilm", "bulldog"]
    """
    scores = {word: word_to_score(word) for word in candidates}
    candidates = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    return [candidate for candidate, score in candidates]


def word_to_score(word: str) -> float:
    return sum(LETTER_FREQUENCIES_FR[letter] for letter in word) / len(word)
