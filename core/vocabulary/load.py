from common.string_utils import fullmatch_regex


def load_wordlist(path_file_wordlist: str):
    with open(path_file_wordlist, "r") as fp:
        data = fp.readlines()

    data = map(lambda word: word.strip().lower(), data)
    data = filter(lambda word: fullmatch_regex(word), data)

    return set(data)
