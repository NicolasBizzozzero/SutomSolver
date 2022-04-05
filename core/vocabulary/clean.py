from core.vocabulary.load import load_wordlist
from core.vocabulary.save import save_wordlist


def clean_wordlist(path_file_wordlist: str):
    wordlist_toclean = load_wordlist(path_file_wordlist=path_file_wordlist)
    wordlist_toclean = sorted(wordlist_toclean)
    save_wordlist(path_file_wordlist=path_file_wordlist, words=wordlist_toclean)
