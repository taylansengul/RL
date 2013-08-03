import pygame as pg
import data


class MapState(object):
    def __init__(self):
        self.name = 'map state'

    def init(self, sys):
        sys.logger.add_message('Dungeon Level 1.')
        sM = sys.stateManager
        gE = sys.graphics_engine
        for name, size in data.Screens.screen_size[sM.currentState.name].iteritems():
                gE.screens[name] = pg.Surface(size)

    def get_display_info(self, sys):
        info = [sys.game_world.objects.player.get_display_info()]  # player info
        info.extend(sys.time.get_display_info())    # turn info
        return info

    def determineAction(self, sys, event):
        player = sys.game_world.objects.player
        game_world = sys.game_world
        sys.event_log.append(event)
        if event in ['move left', 'move right', 'move up', 'move down']:
            if sys.event_log[-2] == 'close door':
                player.close_door(game_world, sys, event)
            else:
                player.move(game_world, sys, event)
                sys.time.new_turn()
                player.hunger.change_current(-1)
        elif event == 'inventory':
            sys.stateManager.changeState(sys.stateManager.inventoryState, sys)
        elif event == 'pick up item':
            tile = sys.game_world.get_tile(player.coordinates)
            if tile.objects_:  # if there is an item on the tile
                for item_ in tile.objects_:
                    if item_.isPickable:
                        player.pick_up_item(item_)
                        tile.remove_object(item_)
                        break
            else:
                return
        elif event == 'drop item':
            tile = sys.game_world.get_tile(player.coordinates)
            item = player.inventory[0]
            if item:
                player.drop_item(item)
                tile.add_object(item)
        elif event == 'make door':
            player.make_door(game_world)
        elif event == 'quit':
            sys.stateManager.changeState(sys.stateManager.quittingState, sys)
        # update player status
        player.update_status(sys)
        # ai action
        sys.ai.determine_total_action(sys)

    def updateScreen(self, sys):
        game_world = sys.game_world
        objects = sys.game_world.objects
        graphics = sys.graphics_engine
        info = self.get_display_info(sys)

        render_update_list = []
        # game world
        # clear game world
        graphics.screens['map'].fill(data.Colors.palette['black'])
        # add game map to render list
        render_update_list.append(graphics.screens['map'].get_rect())
        for tile in game_world.tiles_list:
            coordinates = graphics.get_screen_position_of(tile.coordinates)
            icon = tile.icon
            color = tile.color
            graphics.fontMgr.Draw(graphics.screens['map'], 'arial', 36, icon,
                                  coordinates, color, 'center', 'center', True)
            if tile.has_objects():
                for item_ in tile.objects_:
                    graphics.fontMgr.Draw(graphics.screens['map'], 'arial', 36, item_.icon,
                                          coordinates, item_.color, 'center', 'center', True)

        # logger messages
        if sys.logger.has_unhandled_messages():
            graphics.display_messages(sys)
            render_update_list.append(graphics.screens['messages'].get_rect())

        # render all the other info
        graphics.render_info(sys, info)

        # always update player info screen #todo
        render_update_list.append(graphics.screens['player'].get_rect())
        graphics.screens['main'].blit(graphics.screens['map'], (0, 0))
        pg.display.update(render_update_list)