import globals as g


class Targeting_State(object):
    def __init__(self, game):
        self.ID = g.StateID.TARGETING
        self.game = game
        self.selected_tile = None
        self.highlighted_tile = None
        self.screens = None

    def init(self):
        self.screens = self.game.state_manager.map_state.screens
        self.selected_tile = None
        self.highlighted_tile = self.game.objects_handler.player.tile

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event in ['left', 'right', 'up', 'down']:
            self.highlighted_tile = self.game.game_world.dungeon.get_neighbor_tile(self.highlighted_tile, event)
        elif event == 'select':
            self.selected_tile = self.highlighted_tile
            self.game.state_manager.change_state(self.game.state_manager.map_state)

    def updateScreen(self):
        self.game.state_manager.map_state.updateScreen()
        coordinates = self.highlighted_tile.get_screen_position()
        screen = self.screens['map']
        self.game.pygame.draw.rect(screen.surface, self.game.data.colors.palette['yellow'], coordinates, 5)  # tile border
        screen.render()
        self.game.pygame.display.flip()