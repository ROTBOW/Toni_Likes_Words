from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from words import words
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

    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(r'https://www.wordhell.net/')
        sleep(0.5)
        self.__close_splash()

        self.buttons = self.__get_letters()
    

    



# toni = Toni()
