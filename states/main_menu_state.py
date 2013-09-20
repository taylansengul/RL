from globals import *
from graphics.menu import Menu
from systems.logger import Logger
from systems.objects_handler import Objects_Handler
from systems.IO import IO
from systems import draw
import data
from entities.dungeon import Dungeon


class Main_Menu_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = MAIN_MENU_STATE
        self.screens = {MAIN_MENU_SCREEN: None}

    def init(self):
        self.options = [
            "NEW GAME",
            "LOAD GAME",
            "QUIT GAME"]
        self.menu = Menu(screen=self.screens[MAIN_MENU_SCREEN],
                         options=self.options,
                         font=MAIN_MENU_FONT,
                         line_height=60
                         )
        self.updateScreen()

    def updateScreen(self):
        draw.menu(self.menu)
        self.screens[MAIN_MENU_SCREEN].render_to_main()
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
                self.game.change_state(self.game.map_state)
            elif option == "LOAD GAME":
                pass
            elif option == "QUIT GAME":
                self.game.is_in_loop = False

    # PRIVATE METHODS
    def _init_game_run(self):
        # initialize dungeon-run related things

        self.game.event_log = [None]  # todo: clear

        kwargs = data.level_design.dungeon_level_1

        self.game.game_world = Dungeon(kwargs)
        self.game.game_world.create_map()

        self.game.objects_handler = Objects_Handler(self.game)

        # entities
        self.game.objects_handler.create_player()  # create player
        # self.game.objects_handler.create_player_items()  # create player items
        self.game.objects_handler.populate_game_items()  # populate game world with game items
        self.game.objects_handler.populate_NPCs()  # populate game world with NPCs

        # todo: AI

        Logger.add_message('Welcome to the dungeons.')