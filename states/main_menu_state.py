import enums
from graphics.menu import Menu
from systems.logger import Logger
from systems.objects_handler import ObjectsHandler
from systems import draw
import data
from entities.dungeon import Dungeon
from entities.game_world import Game_World
import base_state


class MainMenuState(base_state.BaseState):
    def __init__(self):
        super(MainMenuState, self).__init__(enums.MAIN_MENU_STATE)
        self.menu = None
        self.options = None

    def init(self):
        super(MainMenuState, self).init()
        self.options = [
            "NEW GAME",
            "LOAD GAME",
            "QUIT GAME"]
        self.menu = Menu(screen=enums.MAIN_MENU_SCREEN,
                         options=self.options,
                         font=enums.MAIN_MENU_FONT,
                         line_height=60
                         )

    def update_screen(self):
        draw.menu(self.menu)
        draw.update()

    def determine_action(self):
        super(MainMenuState, self).determine_action()
        event = self.get_event()
        if event == 'down':
            self.menu.next()
        elif event == 'up':
            self.menu.prev()
        elif event == 'select':
            self._option_selected()

    # ============PRIVATE METHODS============
    def _option_selected(self):
        option = self.menu.highlighted_option
        if option == "NEW GAME":
            self._init_game_run()
            self.next_game_state = enums.MAP_STATE
        elif option == "LOAD GAME":
            pass
        elif option == "QUIT GAME":
            self.next_game_state = "QUIT GAME"

    @staticmethod
    def _init_game_run():
        # initialize dungeon-run related things
        kwargs = data.level_design.dungeon_level_1
        Game_World.dungeon = Dungeon(kwargs)
        # entities
        ObjectsHandler.create_player()  # create player
        ObjectsHandler.populate_game_items()  # populate game world with game items
        ObjectsHandler.populate_NPCs()  # populate game world with NPCs
        # todo: AI
        Logger.add('Welcome to the dungeons.')