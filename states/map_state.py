import os


class Map_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = 'map state'
        self.screens = {'map': None, 'player': None, 'game info': None, 'messages': None, 'enemy': None}
        self.images = {}

    def init(self):
        image_location = os.path.join('images', "floor_tile.png")
        self.images['floor'] = self.game.pygame.image.load(image_location).convert_alpha()
        self.updateScreen()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        player = self.game.objects_handler.player
        game_world = self.game.game_world
        tile = player.tile
        self.game.event_log.append(event)

        if event in ['up', 'down', 'left', 'right']:
            target_tile = game_world.dungeon.get_neighbor_tile(tile, event)
            if not target_tile or 'movement blocking' in target_tile.properties:  # target not valid or movement blocking
                self.game.io_handler.set_active_event(None)
            elif self.game.event_log[-2] == 'close door':
                player.close_door(event)
            elif target_tile.tip == 'closed door':  # target tile = closed door
                player.open_door()
            elif target_tile.has_an_object_which_is('NPC'):
                NPC = target_tile.objects[0]
                player.attack_to(NPC)
                NPC.attack_to(player)
            else:  # if the target tile is a valid tile.
                player.move(target_tile)  # move
        elif event == 'descend' and tile.tip == 'exit':
            self.game.logger.game_over_message = 'Congratulations. You found the way out.'
            self.game.state_manager.change_state(self.game.state_manager.game_over_screen_state)
        elif event == 'inventory':
            self.game.state_manager.inventory_state.key = ''
            self.game.state_manager.change_state(self.game.state_manager.inventory_state)
        elif event == 'eat item':
            self.game.state_manager.inventory_state.key = 'edible'
            self.game.state_manager.change_state(self.game.state_manager.inventory_state)
            item = self.game.state_manager.inventory_state.selected_item
            if item:
                player.consume(item)
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
        elif event == 'target':
            self.game.state_manager.change_state(self.game.state_manager.targeting_state)
        elif event == 'quit':
            self.game.state_manager.change_state(self.game.state_manager.main_menu_state)

    def updateScreen(self):
        game_world = self.game.game_world
        for ID in self.screens:
            self.screens[ID].clear()

        # game world
        # clear game world
        ms = self.screens['map']
        ms.clear()
        # add game map to render list
        x1, y1 = self.game.objects_handler.player.tile.coordinates
        coordinates_list = game_world.dungeon.get_all_neighbors_coordinates((x1, y1), 10)
        coordinates_list.append((x1, y1))
        for x2, y2 in coordinates_list:
            tile = game_world.dungeon.map2D[x2][y2]
            if not tile.is_explored:
                continue
            coordinates = tile.get_screen_position()
            color = tile.color
            if tile.tip == 'floor':
                ms.surface.blit(self.images['floor'], coordinates)
            else:
                self.game.pygame.draw.rect(ms.surface, color, coordinates)  # tile background
            self.game.pygame.draw.rect(ms.surface, self.game.data.colors.palette['white'], coordinates, 1)  # tile border

            if 'container' in tile.properties:
                for item in tile.objects:
                    self.game.font_manager.Draw(ms.surface, 'arial', 36, item.icon,
                                          coordinates, item.color, 'center', 'center', True)

        # logger messages
        if self.game.logger.has_unhandled_messages():
            self.game.logger.display_messages()

        # render all the other info
        # obtain info to display
        self.game.objects_handler.player.render_stats()  # display player stats
        self.game.time.render_turn()    # display turn info

        # always update player info screen #todo
        ms.render()

        self.game.pygame.display.flip()