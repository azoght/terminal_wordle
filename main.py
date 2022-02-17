import curses  # for terminal functionality and styling
import random  # for randomized generation
from curses import wrapper


with open("wordle_words.txt", "r") as file:  # file taken from Hunspell Dictionary (CA)
    wordle_words = [line.strip() for line in file.readlines()]

stdscr = curses.initscr()


def startscreen(stdscr):  # displays the welcome message on terminal
    stdscr.clear()
    stdscr.addstr("Welcome to ")
    stdscr.addstr("Wordle", curses.color_pair(5))
    stdscr.addstr(" (For Terminal)!")
    stdscr.addstr("\nThe correct word has 5 letters, can you get it right?")
    stdscr.addstr("\nType your guess and hit the ENTER key")
    stdscr.addstr("\nIf a letter is green, it's in the word and in the right position", curses.color_pair(4))
    stdscr.addstr("\nIf a letter is yellow, it's in the word but in the wrong position", curses.color_pair(3))
    stdscr.addstr("\nIf a letter is red, it's not in the word at all!", curses.color_pair(2))
    stdscr.addstr("\nYou have 6 attempts to guess the word. Good luck!")
    stdscr.addstr("\n\nPress ENTER to begin")
    stdscr.refresh()

    while True:
        key = stdscr.getkey()

        if key in ("\r", "\n", "\x0D", "\x0A"):  # will start game once ENTER key is pressed
            break


def display_word(stdscr, target, typed, tries):  # shows how correct a guess is (according to the rules)

    if "".join(typed) in wordle_words:  # checks if guess is a valid word
        for i, char in enumerate(typed):  # checks each individual character if valid
            if char not in target:
                color = curses.color_pair(2)  # non-existent letters are red
            elif char in target and target[i] != typed[i]:
                color = curses.color_pair(3)  # existent letters in wrong place are yellow
            else:
                color = curses.color_pair(4)  # existent letters in right place are green
            stdscr.addstr(8-tries, i+2, char, color)  # puts status above typed character

    done = False  # is the game done?
    valid = True  # is the word valid?

    if "".join(typed) == target:  # if user happens to get word correct...
        stdscr.addstr(9, 0, "Correct! Well done!")
        stdscr.addstr(11, 0, "Press ENTER to exit")
        done = True

    elif "".join(typed) not in wordle_words:  # if the word is invalid...
        stdscr.addstr(9, 0, "Not in list")
        valid = False

    elif tries == 1:  # if no tries are left...
        stdscr.addstr(9, 0, f"Too bad, so sad, the correct word was {target}... Good game!")
        stdscr.addstr(11, 0, "Press ENTER to exit")
        done = True

    else:
        stdscr.addstr(7, 0, "                 ")  # clears out the space

    return done, valid


def wordle_game(stdscr, target, tries):

    current_word = []
    x = True

    while x:
        stdscr.addstr(0, 0, "--WORDLE--")

        stdscr.addstr(8-tries, 2, "".join(current_word))  # for each try, new row, but indented to align with title

        key = stdscr.getkey()

        if ord(key) == 27:
            break
        if key in ("BACKSPACE", "\b", "\x7f"):  # deletes letter from word on BACKSPACE
            if len(current_word) > 0:
                current_word = current_word[:-1]
        elif key in ("\r", "\n", "\x0D", "\x0A"):  # "submits" guess when ENTER key hit
            x = False
        else:
            if len(current_word) < 5:  # word can only be five letters
                current_word.append(key)

    return display_word(stdscr, target, current_word, tries)  # ready to verify


def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # default
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # incorrect letter
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # correct letter, wrong position
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)  # correct letter, right position
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)  # name of game

    startscreen(stdscr)

    stdscr.clear()

    correct_word = random.choice(wordle_words)
    tries = 6

    while True:
        d, v = wordle_game(stdscr, correct_word, tries)  # will return True when game ends so user can exit

        if v:  # will only count down if word is in list
            tries -= 1

        if d:
            key = stdscr.getkey()

            if key in ("\r", "\n", "\x0D", "\x0A"):  # ENTER key to exit
                break


wrapper(main)  # main loop
