#! pygamenv/bin/python
"""run a new game"""
import random

import enums
from game import Game
from graphics.screen import Screen


# initialize random numbers
from systems.debuger import debuger

seed_value = 0  # make this None to use the system time as a seed_value
random.seed(seed_value)
# initialize screen_dict
Screen.initialize_screens()
game = Game()
game.current_state = enums.MAIN_MENU_STATE
game.loop()
debuger.debug("Exit to OS")