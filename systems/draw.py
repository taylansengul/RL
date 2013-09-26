from graphics.screen import Screen

__author__ = 'Taylan Sengul'
import pygame
import os
from graphics.text import Text
from enums import *
from logger import Logger


def dungeon(player, screen):
    for tile in player.tiles_in_visibility_radius:
        if tile.is_explored:
            entity(tile, screen)
            if 'container' in tile.properties:
                for each in tile.container:
                    entity(each, screen)
        Screen.dictionary[screen].render_to_main()


def draw_tile_border(tile, screen):
    pygame.draw.rect(screen, WHITE, tile.screen_position, 1)


def entity(entity, screen):
    if entity.image:
        image_location = os.path.join('images', entity.image)
        image = pygame.image.load(image_location).convert_alpha()
        Screen.dictionary[screen].surface.blit(image, entity.tile.screen_position)
    else:
        t = Text(screen=screen,
                 font='map object',
                 context=entity.icon,
                 coordinates=entity.tile.screen_position,
                 color=entity.color,
                 horizontal_align='center',
                 vertical_align='center')
        t.render()


def description(entity, screen):
    Screen.dictionary[screen].clear()
    context = entity.description
    t = Text(font=INVENTORY_FONT, screen=screen, context=context, coordinates=(0, 0), color='white')
    t.render()
    Screen.dictionary[screen].render_to_main()


def menu(menu_to_draw):
    Screen.dictionary[menu_to_draw.screen].clear()
    if len(menu_to_draw) == 0:
        t = Text(
            screen=menu_to_draw.screen,
            context=menu_to_draw.empty_menu_message,
            coordinates=(menu_to_draw.left_padding, menu_to_draw.top_padding),
            color=menu_to_draw.normal_option_color,
            font=menu_to_draw.font)
        t.render()

    for j, option in enumerate(menu_to_draw):
        color = [menu_to_draw.normal_option_color, menu_to_draw.highlighted_option_color][j == menu_to_draw.highlighted_option_index]
        t = Text(
            screen=menu_to_draw.screen,
            context=option,
            coordinates=(menu_to_draw.left_padding, j*menu_to_draw.line_height + menu_to_draw.top_padding),
            color=color,
            font=menu_to_draw.font)
        t.render()
    Screen.dictionary[menu_to_draw.screen].render_to_main()


def inventory_description(item):
    if not item:
        return
    description(item, INVENTORY_DETAILS_SCREEN)


def inventory_menu(menu_to_draw):
    screen = Screen.dictionary[INVENTORY_MENU_SCREEN]
    screen.force_screen_update()
    menu(menu_to_draw)


def player_stats(player):
    line_height = 16
    contexts = [
        player.name,
        'hp: %2.1f/%d' % (player.hp.current, player.hp.maximum),
        'hunger: %d/%d' % (player.hunger.current, player.hunger.maximum)]
    l = len(contexts)
    screens = [PLAYER_SCREEN]*l
    coordinates = [(0, j*line_height) for j in range(l)]
    colors = ['white']*l
    for _ in zip(screens, contexts, coordinates, colors):
        t = Text(font=CONSOLE_FONT, screen=_[0], context=_[1], coordinates=_[2], color=_[3])
        t.render()


def game_over_messages():
    screen = Screen.dictionary[GAME_OVER_SCREEN]
    screen.clear()
    line_height = 40
    contexts = [
        'Game is over.',
        Logger.game_over_message,
        'Press Space.']
    l = len(contexts)

    screens = [GAME_OVER_SCREEN]*l
    coordinates = [(0, j*line_height) for j in range(l)]
    colors = ['white']*l
    for _ in zip(screens, contexts, coordinates, colors):
        t = Text(font=CONSOLE_FONT, screen=_[0], context=_[1], coordinates=_[2], color=_[3])
        t.render()
    update()


def render_turn(turn_info, screen):
    t = Text(screen=screen,
             context='turn: %d' % turn_info, font=CONSOLE_FONT, coordinates=(0, 0), color='white')
    t.render()


def update():
    pygame.display.flip()


def highlighted_tile_border(coordinates):
    """
    draw a highlighted tile border at the given coordinates
    :param coordinates: tuple
    """
    screen = MAP_SCREEN
    screen_object = Screen.dictionary[screen]
    pygame.draw.rect(screen_object.surface, YELLOW, coordinates, 5)  # tile border
    screen_object.render_to_main()


def messages_screen():
    #todo: refactor display_messages
    screen = MESSAGES_SCREEN
    if not Logger._has_unhandled_messages():
        return
    new_line_height = 12
    x, y = Screen.dictionary[screen].width, Screen.dictionary[screen].height
    while Logger._has_unhandled_messages():
        Logger._handle_message()

    Screen.dictionary[screen].clear()
    for co, message in enumerate(Logger.message_archive[-4:]):
        c = pygame.Rect(0, new_line_height*co, x, y)
        t = Text(screen=screen, font=CONSOLE_FONT, context=message, coordinates=c, color='white')
        t.render()


def clear_all_screens():
    Screen.dictionary[MAP_SCREEN].clear()
    Screen.dictionary[ENEMY_SCREEN].clear()
    Screen.dictionary[PLAYER_SCREEN].clear()
    Screen.dictionary[MESSAGES_SCREEN].clear()