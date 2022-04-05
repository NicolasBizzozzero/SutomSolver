import re
from functools import partial

from common.string_utils import fullmatch_regex
from core.strategy.most_common_letters import most_common_letters
from core.strategy.most_different_letters import most_different_letters
from core.vocabulary.load import load_wordlist

PATH_FILE_WORDLIST = "data/wordlist_fr.txt"


class Solver:
    def __init__(
        self,
        nb_letters: int,
        first_letter: str,
        path_file_wordlist: str = PATH_FILE_WORDLIST,
    ):
        self.nb_letters: int = nb_letters
        self.vocabulary: set = load_wordlist(path_file_wordlist=path_file_wordlist)
        self.good_positions = {first_letter: set([0])}  # Red letters
        self.bad_positions = dict()  # Yellow letters
        self.not_here = set()  # Greyed letters

        self._filter_by_length(length=self.nb_letters)
        self._filter_by_first_letter(letter=first_letter)

    def __str__(self):
        word = ""
        for idx_letter in range(self.nb_letters):
            for letter, positions in self.good_positions.items():
                if idx_letter in positions:
                    word += letter
                    break
            else:
                word += "."
        return f"""Solver(
    remaining_candidates: {len(self.vocabulary)}
    word: {word}
    bad_positions: {self.bad_positions}
    not_here: {self.not_here}
)
        """

    def get_prediction(self):
        candidates = sorted(self.vocabulary)
        candidates = most_different_letters(candidates=candidates)
        candidates = most_common_letters(candidates=candidates)

        next_word = candidates[0]
        return next_word

    def delete_word(self, word: str):
        self.vocabulary.remove(word)

    def delete_candidates(self, result: dict):
        self._update_letter_information(result)

        # Compute all unusable letters
        not_here = "".join(self.not_here)

        # Build Regex following good_positions patterns
        regex = ""
        for idx_letter in range(self.nb_letters):
            for letter, positions in self.good_positions.items():
                if idx_letter in positions:
                    regex += letter
                    break
            else:
                # This letter is unknown, add good letters but at the wrong position
                _not_here = not_here
                for letter, positions in self.bad_positions.items():
                    if idx_letter in positions:
                        _not_here += letter
                regex += f"[^{_not_here}]"

        regex = re.compile(regex)

        # We have regex, now delete candidates not matching it
        self._filter_by_regex(regex=regex)

    def _filter_by_length(self, length: int):
        self.vocabulary = set(word for word in self.vocabulary if len(word) == length)

    def _filter_by_first_letter(self, letter: str):
        self.vocabulary = set(word for word in self.vocabulary if word[0] == letter)

    def _filter_by_regex(self, regex):
        func = partial(fullmatch_regex, regex=regex)
        self.vocabulary = set(filter(func, self.vocabulary))

    def _update_letter_information(self, result):
        for letter in result["good_positions"]:
            if letter in self.good_positions.keys():
                self.good_positions[letter].add(result["good_positions"][letter])
            else:
                self.good_positions[letter] = set([result["good_positions"][letter]])
        for letter in result["bad_positions"]:
            if letter in self.bad_positions.keys():
                self.bad_positions[letter].add(result["bad_positions"][letter])
            else:
                self.bad_positions[letter] = set([result["bad_positions"][letter]])
        self.not_here.update(set(result["not_here"]))
