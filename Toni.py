# import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as ac

from words import words  # this is just a set of a lot of five letter words.


class Toni:
    
    def __tprint(self, string: str) -> None:
        print(f'Toni:', string)
        
    def __pretty_format(self) -> str:
        pformat = list()
        for i in range(1, 6):
            pformat.append(
                f'\t{i} - {self.word_letters[i][0]} - {self.word_letters[i][1]}'
            )
            
        return '\n'.join(pformat)

    def __close_splash(self) -> None:
        self.__tprint('Lets get that splash out of the way')
        self.driver.find_element(By.XPATH, '//button[text()="Play"]').click()
    
        self.driver.find_element(By.CSS_SELECTOR, 'h2 + button').click()


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
            file.write(f'{len(self.pool)} possible words\n')
            file.write(f'{self.__pretty_format()}\n')
            file.write('last word tried: ')
            for item in self.pool:
                file.write(f'{item}\n')

    def start_session(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(2)
        self.driver.get(r'https://www.nytimes.com/games/wordle/index.html')
        self.__close_splash()
        

    def __init__(self) -> None:
        self.__tprint('Just getting some things setup, one sec')
        self.row = 1
        self.pool = words
        self.curr_word = str()
        self.word_letters = {
            1: ['', set()],
            2: ['', set()],
            3: ['', set()],
            4: ['', set()],
            5: ['', set()],
        }

    def ban(self, idx: int, letter: str) -> None:
        self.word_letters[int(idx)][1].add(letter)
        
    def ban_letter(self, letter: str) -> None:
        for i in range(1, 6):
            self.word_letters[i][1].add(letter)

    def ban_word(self, word: str) -> None:
        for idx, letter in enumerate(word):
            self.word_letters[idx+1][1].add(letter)

    def ensure_letter(self, idx: int, letter: str) -> None:
        self.word_letters[int(idx)][0] = letter
        
    def clear_row(self) -> None:
        self.__tprint("oops not a word, clearing it now!")
        actions = ac(self.driver)
        for _ in range(5):
            actions.send_keys(Keys.BACKSPACE).perform()
        sleep(.5)

    def update_from_row(self, r: int) -> None:
        row = self.driver.find_element(By.XPATH, f'//div[@aria-label="Row {r}"]')
        tiles = row.find_elements(By.CSS_SELECTOR, '[aria-roledescription="tile"]')
        
        self.__tprint('Updating what I know about the word!')
        for tile in tiles:
            data = tile.get_attribute('aria-label').split(',')
            # if the len of data isn't 3, that means it a word that isn't on the list
            # we can stop the method and the main loop should just keep trying the next words on our list
            if len(data) != 3:
                return self.clear_row()
            
            # rip the data we need, letter, pos, and state
            idx = data[0][0]
            letter = data[1].strip().lower()
            state = data[2].strip().lower()
            
            # use said data to update our word_letters
            if state == 'absent':
                self.ban_letter(letter)
            elif state == 'correct':
                self.ensure_letter(idx, letter)
            else:
                # meaning its present, just not at this spot
                self.ban(idx, letter)
        # after this has been ran, then we're done with this row and can start the next one
        self.row += 1
        sleep(2)
        

    def guess(self) -> str:
        # gen our pool, based on the info stored in word_letters
        self.pool = self.__filter_words()
        self.__write_pool() # writes current pool to the txt file
        
        # type in the current word and submit it
        self.curr_word = self.pool.pop()
        
        actions = ac(self.driver)
        actions.send_keys(self.curr_word).send_keys(Keys.ENTER).perform()
    
    
    def check_if_over(self) -> bool:
        try:
            # looking for the input for email, when you win they ask you to create a account
            self.driver.find_element(By.XPATH, '//fieldset[@type="email"]')
            return True
        except:
            return False

    def play(self) -> None:
        self.start_session()
        playing = True
        while playing:
            # make guess and update our word_letters as needed
            self.guess()
            self.update_from_row(self.row)
            
            if self.check_if_over():
                playing = False
                continue
            
        if self.row <= 5:
            self.__tprint(f'GOT IT~ heck yeah boi, i\'m so freaking good at this - oh the word was {self.curr_word}')
        else:
            self.__tprint(f'Alrighty! all done, not sure if I won or not haha... my last guess was {self.curr_word}')
            
            


if __name__ == '__main__':
    toni = Toni()
    toni.play()

