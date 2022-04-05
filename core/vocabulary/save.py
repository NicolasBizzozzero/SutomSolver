def save_wordlist(path_file_wordlist: str, words: list[str]):
    with open(path_file_wordlist, "w") as fp:
        fp.writelines(words)
