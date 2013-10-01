import os

import pygame

from enums import *
from graphics.screen import Screen
from graphics.text import Text
from logger import Logger


def draw_tile_objects(tile, screen):
    if 'container' not in tile.properties:
        return
    for each in tile.container:
        draw_entity(each, screen)


def draw_tiles(tiles, screen):
    for tile in tiles:
        draw_entity(tile, screen)
        draw_tile_objects(tile, screen)
        Screen.dictionary[screen].render_to_main()


def draw_tile_border(tile, screen):
    pygame.draw.rect(screen, WHITE, tile.screen_position, 1)


def draw_entity(given_entity, screen):
    if given_entity.image:
        image_location = os.path.join('images', given_entity.image)
        image = pygame.image.load(image_location).convert_alpha()
        Screen.dictionary[screen].surface.blit(image, given_entity.tile.screen_position)
    else:
        t = Text(screen=screen,
                 font='map object',
                 context=given_entity.icon,
                 coordinates=given_entity.tile.screen_position,
                 color=given_entity.color,
                 horizontal_align='center',
                 vertical_align='center')
        t.render()


def highlight_tile_border(coordinates):
    """
    draw a highlighted tile border at the given coordinates
    :param coordinates: tuple
    """
    screen = MAP_SCREEN
    screen_object = Screen.dictionary[screen]
    pygame.draw.rect(screen_object.surface, YELLOW, coordinates, 5)  # tile border
    screen_object.render_to_main()


def draw_inventory_description(entity):
    screen = INVENTORY_DETAILS_SCREEN
    Screen.dictionary[screen].clear()
    context = entity.description
    t = Text(
        font=INVENTORY_FONT,
        screen=screen,
        context=context,
        coordinates=(0, 0),
        color='red')
    t.render()
    Screen.dictionary[screen].render_to_main()


def draw_menu(menu):
    Screen.dictionary[menu.screen].clear()
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
            coordinates=(menu.left_padding, j * menu.line_height + menu.top_padding),
            color=color,
            font=menu.font)
        t.render()
    Screen.dictionary[menu.screen].render_to_main()


def draw_inventory_menu(menu_to_draw):
    screen = Screen.dictionary[INVENTORY_MENU_SCREEN]
    screen.force_screen_update()
    draw_menu(menu_to_draw)


def draw_player_stats(player):
    line_height = 16
    contexts = [
        player.name,
        'hp: %2.1f/%d' % (player.hp.current, player.hp.maximum),
        'hunger: %d/%d' % (player.hunger.current, player.hunger.maximum)]
    l = len(contexts)
    screens = [PLAYER_SCREEN] * l
    coordinates = [(0, j * line_height) for j in range(l)]
    colors = ['white'] * l
    for _ in zip(screens, contexts, coordinates, colors):
        t = Text(font=CONSOLE_FONT, screen=_[0], context=_[1], coordinates=_[2], color=_[3])
        t.render()


def draw_game_over_messages():
    screen = Screen.dictionary[GAME_OVER_SCREEN]
    screen.clear()
    line_height = 40
    contexts = [
        'Game is over.',
        Logger.game_over_message,
        'Press Space.']
    l = len(contexts)

    screens = [GAME_OVER_SCREEN] * l
    coordinates = [(0, j * line_height) for j in range(l)]
    colors = ['white'] * l
    for _ in zip(screens, contexts, coordinates, colors):
        t = Text(font=CONSOLE_FONT, screen=_[0], context=_[1], coordinates=_[2], color=_[3])
        t.render()
    update()


def draw_turn(turn_info, screen):
    t = Text(screen=screen,
             context='turn: %d' % turn_info,
             font=CONSOLE_FONT,
             coordinates=(0, 0),
             color='white')
    t.render()


def update():
    pygame.display.flip()


def messages_screen(messages):
    kwargs = {
        'font': CONSOLE_FONT,
        'font color': WHITE,
        'screen': MESSAGES_SCREEN,
        'line spacing': 12,
        'texts': messages
    }
    text_screen(kwargs)


def clear_all_screens():
    Screen.dictionary[MAP_SCREEN].clear()
    Screen.dictionary[ENEMY_SCREEN].clear()
    Screen.dictionary[PLAYER_SCREEN].clear()
    Screen.dictionary[MESSAGES_SCREEN].clear()
    Screen.dictionary[GAME_INFO_SCREEN].clear()


def text_screen(kwargs):
    screen = kwargs['screen']
    font = kwargs['font']
    color = kwargs['font color']
    line_spacing = kwargs['line spacing']
    texts = kwargs['texts']
    Screen.dictionary[screen].clear()
    x, y = Screen.dictionary[screen].width, Screen.dictionary[screen].height
    for co, text in enumerate(texts):
        c = pygame.Rect(0, line_spacing*co, x, y)
        t = Text(
            screen=screen,
            font=font,
            context=text,
            coordinates=c,
            color=color)
        t.render()
