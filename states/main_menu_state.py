from globals import *
from graphics.menu import Menu
from systems.logger import Logger
from systems.objects_handler import Objects_Handler
from systems.IO import IO
from systems import draw
import data
from entities.dungeon import Dungeon
from entities.game_world import Game_World


class Main_Menu_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = MAIN_MENU_STATE

    def init(self):
        self.options = [
            "NEW GAME",
            "LOAD GAME",
            "QUIT GAME"]
        self.menu = Menu(screen=MAIN_MENU_SCREEN,
                         options=self.options,
                         font=MAIN_MENU_FONT,
                         line_height=60
                         )
        self.updateScreen()

    def updateScreen(self):
        draw.menu(self.menu)
        draw.update()

    def determineAction(self):
        event = IO.active_event
        if event == 'down':
            self.menu.next()
        elif event == 'up':
            self.menu.prev()
        elif event == 'select':
            option = self.menu.highlighted_option
            if option == "NEW GAME":
                self._init_game_run()
                self.game.change_state(MAP_STATE)
            elif option == "LOAD GAME":
                pass
            elif option == "QUIT GAME":
                self.game.is_in_loop = False

    # PRIVATE METHODS
    def _init_game_run(self):
        # initialize dungeon-run related things


        kwargs = data.level_design.dungeon_level_1

        Game_World.dungeon = Dungeon(kwargs)

        # entities
        Objects_Handler.create_player()  # create player
        Objects_Handler.populate_game_items()  # populate game world with game items
        Objects_Handler.populate_NPCs()  # populate game world with NPCs

        # todo: AI

        Logger.add_message('Welcome to the dungeons.')