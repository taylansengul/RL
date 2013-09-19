__author__ = 'Taylan Sengul'
import pygame
import os
from graphics.text import Text
from globals import *
from logger import Logger


class Draw:
    @staticmethod
    def dungeon(player, screen):
        for tile in player.tiles_in_visibility_radius:
            if tile.is_explored:
                Draw.entity(tile, screen)
                if 'container' in tile.properties:
                    for each in tile.container:
                        Draw.entity(each, screen)
        screen.render_to_main()


    @staticmethod
    def entity(entity, screen):
        if entity.image:
            image_location = os.path.join('images', entity.image)
            image = pygame.image.load(image_location).convert_alpha()
            screen.surface.blit(image, entity.tile.screen_position)
        else:
            t = Text(screen=screen,
                     font='map object',
                     context=entity.icon,
                     coordinates=entity.tile.screen_position,
                     color=entity.color,
                     horizontal_align='center',
                     vertical_align='center')
            t.render()

    @staticmethod
    def description(entity, screen):
        screen.clear()
        context = entity.description
        t = Text(font=INVENTORY_FONT, screen=screen, context=context, coordinates=(0, 0), color='white')
        t.render()
        screen.render_to_main()

    @staticmethod
    def menu(menu):
        menu.screen.clear()
        if len(menu) == 0:
            t = Text(
                screen=menu.screen,
                context=menu.empty_menu_message,
                coordinates=(menu.left_padding, menu.top_padding),
                color=menu.normal_option_color,
                font=menu.font)
            t.render()

        for j, option in enumerate(menu):
            color = [menu.normal_option_color, menu.highlighted_option_color][j == menu.highlighted_option_index]
            t = Text(
                screen=menu.screen,
                context=option,
                coordinates=(menu.left_padding, j*menu.line_height + menu.top_padding),
                color=color,
                font=menu.font)
            t.render()
        menu.screen.render_to_main()


    @staticmethod
    def player_stats(player):
        line_height = 16
        contexts = [player.name,
                    'hp: %2.1f/%d' % (player.hp.current, player.hp.maximum),
                    'hunger: %d/%d' % (player.hunger.current, player.hunger.maximum)]
        l = len(contexts)
        screens = [player.game.map_state.screens[PLAYER_SCREEN]]*l
        coordinates = [(0, j*line_height) for j in range(l)]
        colors = ['white']*l
        for _ in zip(screens, contexts, coordinates, colors):
            t = Text(font=CONSOLE_FONT, screen=_[0], context=_[1], coordinates=_[2], color=_[3])
            t.render()

    @staticmethod
    def game_over_messages(screen):
        screen.clear()
        line_height = 40
        contexts = ['Game is over.',
                    Logger.game_over_message,
                    'Press Space.']
        l = len(contexts)

        screens = [screen]*l
        coordinates = [(0, j*line_height) for j in range(l)]
        colors = ['white']*l
        for _ in zip(screens, contexts, coordinates, colors):
            t = Text(font=CONSOLE_FONT, screen=_[0], context=_[1], coordinates=_[2], color=_[3])
            t.render()