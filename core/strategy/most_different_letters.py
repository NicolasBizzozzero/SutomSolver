def most_different_letters(candidates: list) -> list[str]:
    """Get candidates with the max number of different letters.
    Candidates must all be off the same length.

    >>> most_different_letters(["pirates", "balloon"])
    ["pirates"]
    """
    max_length = max(map(lambda word: len(set(word)), candidates))
    return [word for word in candidates if max_length == len(set(word))]
