import globals as g
from graphics.menu import Menu
from systems.time import Time
from systems.message_logger import MessageLogger
from objects.game_world import Game_World
from systems.objects_handler import Objects_Handler
from systems.resource_manager import Resource_Manager


class Main_Menu_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = g.StateID.MAIN_MENU
        self.screens = {'menu': None}

    def init(self):
        self.options = [
            "NEW GAME",
            "LOAD GAME",
            "QUIT GAME"]
        self.menu = Menu(screen=self.screens['menu'],
                         options=self.options,
                         font=g.FontID.MAIN_MENU
                         )
        self.updateScreen()

    def updateScreen(self):
        self.menu.render()
        self.screens['menu'].render()
        self.game.pygame.display.update()

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
                self.game.state_manager.change_state(self.game.state_manager.map_state)
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
        self.game.objects_handler.populate_NPCs()  # populate game world with NPCS

        # AI: do not need AI
        # self.game.ai = AI(self.game)

        # initialize map and inventory screens
        self.game.state_manager.initialize_screens(g.StateID.INVENTORY)
        self.game.state_manager.initialize_screens(g.StateID.MAP)

        self.game.logger.add_message('Main_Menu_State._init_game_run() finished.')