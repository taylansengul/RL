from systems.time import Time
from systems.stateManager import StateManager
from systems.message_logger import MessageLogger
from systems.graphics_engine import Graphics_Engine
from systems.io_handler import Io_Handler
from objects.game_world import Game_World
from systems import AI


class System(object):
    def __init__(self):
        self.event_log = [None]
        self.time = Time()
        self.stateManager = StateManager()
        self.logger = MessageLogger()
        self.graphics_engine = Graphics_Engine()
        self.io_handler = Io_Handler()
        self.game_world = Game_World()
        self.ai = AI(self.game_world.objects.NPCs)