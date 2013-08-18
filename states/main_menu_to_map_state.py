from systems.time import Time
from systems.message_logger import MessageLogger
from objects.game_world import Game_World
from systems.objects_handler import Objects_Handler
from systems.resource_manager import Resource_Manager
from systems import AI


class Main_Menu_To_Map_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = 'map state'

    def init(self):
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

        self.game.logger.add_message('Menu to Map initialization finished.')

    def determineAction(self):
        pass

    def updateScreen(self):
        pass