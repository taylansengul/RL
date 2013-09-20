from game import Game
import random
from graphics.screen import Screen

__author__ = 'Taylan Sengul'
seed_value = 0  # make this None to use the system time as a seed_value
random.seed(seed_value)
# initialize screen_dict
Screen.initialize_screens()
game = Game()
game.change_state(game.main_menu_state)
game.loop()
game.exit()
del game
