#! pygamenv/bin/python
from game import Game
import random
from graphics.screen import Screen
import globals

__author__ = 'Taylan Sengul'

# initialize random numbers
seed_value = 0  # make this None to use the system time as a seed_value
random.seed(seed_value)
# initialize screen_dict
Screen.initialize_screens()
game = Game()
game.current_state = game.states[globals.MAIN_MENU_STATE]
game.loop()
game.exit()
del game
