from game import Game

__author__ = 'Taylan Sengul'

game = Game()
game.change_state(game.main_menu_state)
game.loop()
game.exit()
del game
