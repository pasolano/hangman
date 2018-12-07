import sys
import random

class Hangman(object):
    def __init__(self, level = 5, non_ascii = False, dictionary = '/usr/share/dict/american', capitals = False, contractions = False): # option(default): level(5), non_ascii(excluded), dictionary(american), capitals(excluded), and contractions(excluded)
        self.level = level
        self.non_ascii = non_ascii
        self.dictionary = dictionary
        self.capitals = capitals
        self.contractions = contractions

    def dict_convert(self):
        with open(self.dictionary, 'r') as file:
            dictionary = file.read().split()
            return dictionary

    def error_modify(self, error_count):
        if error_count == 1:
            self.line2 = '|   0'
        elif error_count == 2:
            self.line3 = '|   |'
        elif error_count == 3:
            self.line3 = '|  /|'
        elif error_count == 4:
            self.line3 = '|  /|\\'
        elif error_count == 5:
            self.line4 = '|  /'
        elif error_count == 6:
            self.line4 = '|  / \\'
            self.game = False

    def did_i_lose(self, letters_guessed, letters, error_count):
        no_spaces = True
        for i in self.letter_list:
            if i == ' ':
                no_spaces = False
                pass
        if no_spaces == True:
            self.game = False
            return self.game
        if error_count == 6:
            self.game = False
            return self.game
        else:
            self.game = True
            return self.game

    def restart_game(self):
        restart = input('Another game? (y/n): ')
        if restart == 'y':
            self.restart = True
        elif restart == 'n':
            self.restart = False
        else: 
            self.restart_game()

    def game_loop(self, answer):
        self.game = True
        self.line2 = '|'
        self.line3 = '|'
        self.line4 = '|'
        error_count = 0
        letters = list(answer)
        self.letter_list = []
        for i in range(0, len(letters)):
            self.letter_list.append(' ')
        letters_guessed = 0
        all_letters_guessed = []
        print('_____\n|   |\n|\n|\n|\n|\n|\n|\n\n' + ('_ ' * len(answer)))
        while self.game == True:
            flag = False
            letter_counter = -1
            letters_str = ''
            invalid_guess = True
            while invalid_guess == True:
                invalid_guess = False
                guess = input('Guess a letter: ')
                if len(guess) != 1:
                    invalid_guess = True
                    print('Enter a letter, not a string!\n')
                for letter in all_letters_guessed:
                    if letter == guess:
                        invalid_guess = True
                        print('You have already guessed \'' + guess + '\'!\n')
            all_letters_guessed.append(guess)
            for letter in letters:
                if guess == letter:
                    letter_counter += 1
                    if self.letter_list[letter_counter] == ' ':
                        self.letter_list[letter_counter] = guess
                    letters_guessed += 1
                    flag = True
                else:
                    letter_counter += 1
            for letter in self.letter_list:
                letters_str += letter + ' '
            if self.did_i_lose(letters_guessed, letters, error_count) == False:
                print('Correct!\n')
                print('_____\n|   |\n' + self.line2 + '\n' + self.line3 + '\n' + self.line4 + '\n|\n|\n|\n' + '\n' + letters_str + '\n' + ('_ ' * len(answer)) + '\n')
                print('You win!\n')
                return
            if flag == False:
                error_count += 1
                self.error_modify(error_count)
                if self.did_i_lose(letters_guessed, letters, error_count) == False:
                    print('Wrong!\n')
                    print('_____\n|   |\n' + self.line2 + '\n' + self.line3 + '\n' + self.line4 + '\n|\n|\n|\n' + '\n' + letters_str + '\n' + ('_ ' * len(answer)) + '\n')
                    print('You lose!  The word was \'' + answer + '\'.\n')
                    return
                else:
                    print('Wrong!\n')
                    print('_____\n|   |\n' + self.line2 + '\n' + self.line3 + '\n' + self.line4 + '\n|\n|\n|\n' + '\n' + letters_str + '\n' + ('_ ' * len(answer)))
            else:
                print('Correct!\n')
                print('_____\n|   |\n' + self.line2 + '\n' + self.line3 + '\n' + self.line4 + '\n|\n|\n|\n' + '\n' + letters_str + '\n' + ('_ ' * len(answer)))

    def play(self):
        self.restart = True
        dictionary = self.dict_convert()
        true_dict = []
        for word in dictionary:
            if len(word) >= self.level:
                true_dict.append(word)
        if self.non_ascii == True:
            for word in true_dict:
                if ord(word) <= 127:
                    true_dict.append(word)
        while self.restart == True:
            valid_answer = False
            while valid_answer == False:
                apostrophe = False
                upper = False
                answer = random.choice(true_dict)
                if self.capitals == False:
                    if answer != answer.lower():
                        upper = True
                if self.contractions == False:
                    for letter in list(answer):
                        if '\'' == letter:
                            apostrophe = True
                if upper == False and apostrophe == False:
                    valid_answer = True
            self.game_loop(answer)
            self.restart_game()
