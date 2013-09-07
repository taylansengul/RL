from game import Game

__author__ = 'Taylan Sengul'

game = Game()
game.state_manager.change_state(game.state_manager.main_menu_state)
game.loop()
game.exit()
del game
