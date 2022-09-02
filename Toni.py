from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from words import words # this is just a set of a lot of five letter words.
from time import sleep


class Toni:

    def __get_letters(self) -> dict:
        res = dict()
        eles = self.driver.find_elements(By.CLASS_NAME, 'keyboard-letter ')
        for ele in eles:
            res[ele.text.lower()] = ele

        return res

    def __close_splash(self) -> None:
        self.driver.find_element(By.CLASS_NAME, 'close-button').click()

    def __click_button(self, button) -> None:
        if button not in self.buttons:
            raise ValueError('That is not a vaild button, vaild buttons are a-z, enter, and del.')
        self.buttons[button].click()

    def __filter_words(self) -> set:
        def filtering(idx, pool):
            res = set()

            for word in pool:
                if word[idx] == self.word_letters[idx+1][0]:
                    res.add(word)
                elif word[idx] not in self.word_letters[idx+1][1]:
                    res.add(word)

            return res

        pool = words
        for idx in range(5):
            pool = filtering(idx, pool)

        return pool

    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(r'https://www.wordhell.net/')
        sleep(0.5)
        self.__close_splash()

        self.buttons = self.__get_letters()

        self.word_letters = {
            1: ['', set()],
            2: ['', set()],
            3: ['', set()],
            4: ['', set()],
            5: ['', set()],
        }

    def type_word(self, word) -> None:
        for letter in word:
            self.__click_button(letter)

    def guess(self) -> None:
        word_pool = self.__filter_words()
        self.type_word(word_pool.pop())
    

    



# toni = Toni()
