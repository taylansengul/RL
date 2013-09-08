from graphics.menu import Menu, Menu_Option
from systems.time import Time
from systems.message_logger import MessageLogger
from objects.game_world import Game_World
from systems.objects_handler import Objects_Handler
from systems.resource_manager import Resource_Manager


class Main_Menu_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = 'main menu state'
        self.screens = {'menu': None}

    def init(self):
        font = self.game.data.fonts.MAIN_MENU
        self.newGameOption = Menu_Option("NEW GAME", (140, 105), font, isHovered=True)
        self.loadGameOption = Menu_Option("LOAD GAME", (140, 155), font)
        self.quitGameOption = Menu_Option("QUIT", (140, 205), font)
        self.menu = Menu(screen=self.screens['menu'],
                         options=[self.newGameOption,
                                  self.loadGameOption,
                                  self.quitGameOption])
        self.updateScreen()

    def updateScreen(self):
        self.menu.draw()
        self.screens['menu'].render()
        self.game.pygame.display.update()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event == 'down':
            self.menu.select_next()
        elif event == 'up':
            self.menu.select_prev()
        elif event == 'select':
            option = self.menu.get_active_option()
            if option == self.newGameOption:
                self._init_game_run()
                self.game.state_manager.change_state(self.game.state_manager.map_state)
            elif option == self.loadGameOption:
                pass
            elif option == self.quitGameOption:
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
        self.game.state_manager.initialize_screens('inventory_state')
        self.game.state_manager.initialize_screens('map_state')

        self.game.logger.add_message('Main_Menu_State._init_game_run() finished.')