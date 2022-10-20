from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from words import words  # this is just a set of a lot of five letter words.


class Toni:

    def __get_letters(self) -> dict:
        res = dict()
        eles = self.driver.find_elements(By.CLASS_NAME, 'keyboard-letter ')
        for ele in eles:
            res[ele.text.lower()] = ele

        return res

    def __close_splash(self) -> None:
        self.driver.find_element(By.CLASS_NAME, 'close-button').click()

    def __click_button(self, button: str) -> None:
        if button not in self.buttons:
            raise ValueError('That is not a vaild button, vaild buttons are a-z, enter, and del.')
        self.buttons[button].click()

    def __filter_words(self) -> set:
        def filtering(idx: int, pool: set) -> set:
            res = set()

            for word in pool:
                if word[idx] == self.word_letters[idx+1][0]:
                    res.add(word)
                elif word[idx] not in self.word_letters[idx+1][1] and self.word_letters[idx+1][0] == '':
                    res.add(word)

            return res

        pool = self.pool
        for idx in range(5):
            pool = filtering(idx, pool)

        return pool

    def __write_pool(self):
        with open('pool.txt', 'w') as file:
            file.write(f'{len(self.pool)} possible words\n{self.word_letters}\n')
            print('last word tried: ', end='')
            for item in self.pool:
                file.write(f'{item}\n')

    def start_session(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(r'https://www.wordhell.net/')
        sleep(0.5)
        self.__close_splash()

        self.buttons = self.__get_letters()

    def __init__(self) -> None:
        self.row = 0
        self.pool = words
        self.word_letters = {
            1: ['', set()],
            2: ['', set()],
            3: ['', set()],
            4: ['', set()],
            5: ['', set()],
        }

    def ban(self, idx: int, letter: str) -> None:
        self.word_letters[idx][1].add(letter)

    def ban_word(self, word: str) -> None:
        for idx, letter in enumerate(word):
            self.word_letters[idx+1][1].add(letter)

    def ensure_letter(self, idx: int, letter: str) -> None:
        self.word_letters[idx][0] = letter

    def type_word(self, word: str) -> None:
        for letter in word:
            self.__click_button(letter)

    def remove_word(self) -> None:
        for _ in range(5):
            self.__click_button('del')

    def get_message(self) -> str:
        sleep(.5)
        try:
            gom = self.driver.find_element(By.ID, 'gameover-message')
            gom.screenshot('text_check.png')
            sleep(1.5)

            if open('t_TAW.png', 'rb').read() == open('text_check.png', 'rb').read():
                gom = 'TAW'
            else:
                gom = 'COR'

        except Exception as err:
            print(err)
            gom = None

        return gom

    def guess(self) -> str:
        self.pool = self.__filter_words()
        self.__write_pool()
        self.type_word(self.pool.pop())
        self.__click_button('enter')
        return self.get_message()

    
    

    def play(self) -> None:
        self.start_session()
        playing = True
        while playing:
            guess = self.guess()
            if guess == 'TAW':
                self.remove_word()
                continue
            
'''
Need to add:
    grabing letters from grid
        getting color for each letter
'''



# toni = Toni()
# print(toni.guess())
