from globals import *
from graphics.menu import Menu
from systems.time import Time
from systems.message_logger import MessageLogger
from objects.game_world import Game_World
from systems.objects_handler import Objects_Handler
from systems.resource_manager import Resource_Manager


class Main_Menu_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = StateID.MAIN_MENU
        self.screens = {ScreenID.MAIN_MENU: None}

    def init(self):
        self.options = [
            "NEW GAME",
            "LOAD GAME",
            "QUIT GAME"]
        self.menu = Menu(screen=self.screens[ScreenID.MAIN_MENU],
                         options=self.options,
                         font=FontID.MAIN_MENU,
                         line_height=60
                         )
        self.updateScreen()
        self.game.refresh_main_screen()

    def updateScreen(self):
        self.menu.render()
        self.screens[ScreenID.MAIN_MENU].render_to_main()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
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
        self.game.event_log = [None]
        self.game.time = Time(self.game)
        self.game.logger = MessageLogger(self.game)
        self.game.game_world = Game_World(self.game)
        self.game.objects_handler = Objects_Handler(self.game)
        self.game.resource_manager = Resource_Manager(self.game)

        # set current dungeon in game world
        self.game.game_world.set_current_dungeon()

        # objects
        self.game.objects_handler.create_player()  # create player
        # self.game.objects_handler.create_player_items()  # create player items
        self.game.objects_handler.populate_game_items()  # populate game world with game items
        self.game.objects_handler.populate_NPCs()  # populate game world with NPCs

        # AI: do not need AI
        # self.game.ai = AI(self.game)

        self.game.logger.add_message('Main_Menu_State._init_game_run() finished.')