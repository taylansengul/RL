import data


class Targeting_State(object):
    def __init__(self, game):
        self.ID = 'targeting state'
        self.game = game
        self.selected_tile = None
        self.highlighted_tile = None

    def init(self):
        self.selected_tile = None
        self.highlighted_tile = self.game.objects_handler.player.tile

    def updateScreen(self):

        self.game.state_manager.map_state.updateScreen()
        coordinates = self.game.graphics_engine.get_screen_position_of(self.highlighted_tile.coordinates)
        self.game.pygame.draw.rect(graphics.screens['map'], data.colors.palette['yellow'], coordinates, 5)  # tile border
        self.game.state_manager.map_state.screens['map'].render()
        self.game.pygame.display.flip()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event in ['left', 'right', 'up', 'down']:
            self.highlighted_tile = self.game.game_world.dungeon.get_neighbor_tile(self.highlighted_tile, event)
        elif event == 'select':
            self.selected_tile = self.highlighted_tile
            self.game.state_manager.change_state(self.game.state_manager.map_state)