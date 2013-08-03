import pygame as pg
import data


class Map_State(object):
    def __init__(self, game):
        self.game = game
        self.name = 'map state'

    def init(self):
        self.updateScreen()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        player = self.game.objects_handler.player
        game_world = self.game.game_world
        tile = self.game.game_world.get_tile(player.coordinates)
        self.game.event_log.append(event)

        move_keys = {'move left': (-1, 0), 'move right': (1, 0), 'move up': (0, -1), 'move down': (0, 1)}
        if event in move_keys.keys():
            x, y = player.coordinates[0] + move_keys[event][0], player.coordinates[1] + move_keys[event][1]
            target_tile = game_world.get_tile((x, y))

            if not target_tile or 'blocks movement' in target_tile.properties:  # target tile not valid or blocks movement
                self.game.io_handler.set_active_event(None)
            elif self.game.event_log[-2] == 'close door':
                player.close_door(event)
            elif target_tile.tip == 'closed door':  # target tile = closed door
                player.open_door()
            else:  # if the target tile is a valid tile.
                player.move(target_tile)  # move
            self.game.time.new_turn()
        elif event == 'descend' and tile.tip == 'exit':
            self.game.state_manager.change_state(self.game.state_manager.game_over_state)
        elif event == 'inventory':
            self.game.state_manager.change_state(self.game.state_manager.inventory_state)
        elif event == 'eat item':
            player.consume(player.objects[0])
        elif event == 'pick up item':
            if tile.has_objects():  # if there is an item on the tile
                for item in tile.objects:
                    if 'pickable' in item.properties:
                        tile.transfer_to(player, item)
                        break
        elif event == 'drop item':
            if player.has_objects():
                item = player.objects[0]
                player.transfer_to(tile, item)
        elif event == 'make door':
            player.make_door(game_world)
        elif event == 'quit':
            self.game.state_manager.change_state(self.game.state_manager.main_menu_state)

    def updateScreen(self):
        game_world = self.game.game_world
        graphics = self.game.graphics_engine

        # game world
        # clear game world
        graphics.screens['map'].fill(data.Colors.palette['black'])
        # add game map to render list
        for tile in game_world.tiles_list:
            if not tile.isVisible:
                continue
            coordinates = graphics.get_screen_position_of(tile.coordinates)
            color = tile.color
            pg.draw.rect(graphics.screens['map'], color, coordinates)
            pg.draw.rect(graphics.screens['map'], data.Colors.palette['white'], coordinates, 1)

            if 'has inventory' in tile.properties:
                for item in tile.objects:
                    graphics.fontMgr.Draw(graphics.screens['map'], 'arial', 36, item.icon,
                                          coordinates, item.color, 'center', 'center', True)

        # logger messages
        if self.game.logger.has_unhandled_messages():
            graphics.display_messages()

        # render all the other info
        # obtain info to display
        info = [self.game.objects_handler.player.get_display_info()]  # player info
        info.extend(self.game.time.get_display_info())    # turn info
        # display info
        graphics.render_info(info)

        # always update player info screen #todo
        graphics.screens['main'].blit(graphics.screens['map'], (0, 0))
        pg.display.flip()