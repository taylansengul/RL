from globals import *
import pygame
from entities.entity import Entity
from systems.IO import IO


class Targeting_State(object):
    def __init__(self, game):
        self.ID = TARGETING_STATE
        self.game = game
        self.selected_tile = None
        self.highlighted_tile = None
        self.screens = None

    def init(self):
        self.screens = self.game.map_state.screens
        self.selected_tile = None
        self.highlighted_tile = Entity.player.tile

    def determineAction(self):
        event = IO.active_event
        if event in ['left', 'right', 'up', 'down']:
            self.highlighted_tile = self.game.game_world.dungeon.get_neighbor_tile(self.highlighted_tile, event)
        elif event == 'select':
            self.selected_tile = self.highlighted_tile
            self.game.change_state(self.game.map_state)

    def updateScreen(self):
        self.game.map_state.updateScreen()
        coordinates = self.highlighted_tile.screen_position
        screen = self.screens[MAP_SCREEN]
        pygame.draw.rect(screen.surface, YELLOW, coordinates, 5)  # tile border
        screen.render_to_main()