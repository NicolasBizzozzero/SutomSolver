import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from collections import Counter
from selenium.webdriver.common.keys import Keys


URL_GAME = r"https://sutom.nocle.fr"


class WebInterface:
    def __init__(self, headless: bool = True, time_sleep: int = 2):
        self.time_sleep = time_sleep
        self.option = webdriver.FirefoxOptions()

        if headless:
            self.option.add_argument("--headless")

        self.driver = webdriver.Firefox(options=self.option, log_path="/dev/null")

        self.round = 1
        self._body = None

    def get_first_round(self):
        self.driver.get(URL_GAME)
        sleep(self.time_sleep)  # The explorer need time to load the game.

        self._close_introduction_window()

        nb_letters = self._get_nb_letters()
        first_letter = self._get_first_letter()

        return nb_letters, first_letter

    def get_result(self, word: str) -> dict:
        self._send_word(word=word)

        # Check if won
        if self._check_won():
            return {"win?": True}

        # Check if word exists from the game's dictionary
        if self._check_word_exists():
            return {"win?": False}
        else:
            # Word exists, now fetch results
            (
                letter_at_good_position,
                letter_at_bad_position,
                letter_not_here,
            ) = self._parse_results()
            self.round += 1
            return {
                "win?": False,
                "good_positions": letter_at_good_position,
                "bad_positions": letter_at_bad_position,
                "not_here": letter_not_here,
            }

    def _send_word(self, word: str):
        self._body = self.driver.find_element(By.XPATH, "/html/body")
        self._body.send_keys(word)
        self._body.send_keys(Keys.ENTER)
        sleep(self.time_sleep)

    def _get_nb_letters(self) -> int:
        return len(
            self.driver.find_element(
                By.XPATH, "/html/body/div/div[@id='grille']/table/tr[1]"
            ).find_elements(By.TAG_NAME, "td")
        )

    def _get_first_letter(self) -> str:
        return (
            self.driver.find_element(By.XPATH, "/html/body/div/div[3]/table")
            .text[0]
            .lower()
        )

    def _close_introduction_window(self):
        self.driver.find_element(By.ID, "panel-fenetre-bouton-fermeture").click()

    def _check_won(self):
        return "Félicitations" in self._body.text

    def _check_word_exists(self):
        return (
            "Ce mot n'est pas dans notre dictionnaire" in self._body.text
            and self._body.find_element(
                By.XPATH, "//*[contains(text(), 'pas dans notre dictionnaire')]"
            ).get_attribute("style")
            == "opacity: 1;"
        )

    def _parse_results(self):
        line = self.driver.find_element(
            By.XPATH, f"/html/body/div/div[3]/table/tr[{self.round}]"
        )
        list_td = line.find_elements(By.TAG_NAME, "td")

        letter_at_good_position = {}
        letter_at_bad_position = {}
        letter_not_here = []

        for td in list_td:
            css_class = td.get_attribute("class")
            position_td = list_td.index(td)
            letter = td.text.lower()

            if css_class == "bien-place resultat":
                letter_at_good_position[letter] = position_td
            elif css_class == "mal-place resultat":
                letter_at_bad_position[letter] = position_td
            elif css_class == "non-trouve resultat":
                letter_not_here.append(letter)
        return letter_at_good_position, letter_at_bad_position, letter_not_here
