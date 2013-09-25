from globals import *
from graphics.menu import Menu
from systems.logger import Logger
from systems.objects_handler import Objects_Handler
from systems import draw
import data
from entities.dungeon import Dungeon
from entities.game_world import Game_World
import base_state


class Main_Menu_State(base_state.BaseState):
    def __init__(self):
        super(Main_Menu_State, self).__init__(MAIN_MENU_STATE)

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

    def update_screen(self):
        draw.menu(self.menu)
        draw.update()

    def determine_action(self):
        super(Main_Menu_State, self).determine_action()
        event = self.get_event()
        if event == 'down':
            self.menu.next()
        elif event == 'up':
            self.menu.prev()
        elif event == 'select':
            option = self.menu.highlighted_option
            self.option_selected(option)

    def option_selected(self, option):
        if option == "NEW GAME":
            self._init_game_run()
            self.next_game_state = MAP_STATE
        elif option == "LOAD GAME":
            pass
        elif option == "QUIT GAME":
            self.next_game_state = "QUIT_STATE"

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