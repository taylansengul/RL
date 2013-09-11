"""
# main screen:
#  divided into two columns, at x = X
#  second column divided into 4 rows at y = Y1, Y1+Y2, Y1+Y2+Y3
#
#              0 ---------X1------X1+X2=W
#               |         |          |
#             Y1|         |----------|
#               |         |          |
#          Y1+Y2|         |----------|
#               |         |          |
#       Y1+Y2+Y3|         |----------|
#               |         |          |
#  H=Y1+Y2+Y3+Y4---------------------
#
"""
import pygame
import globals as g
print __name__, dir()
width = 1200
height = 720
tile_length = 32
X1 = int(.8 * width)
tile_no_x = X1 / tile_length
tile_no_y = height / tile_length
X2 = int(.2 * width)

Y1 = int(.3 * height)
Y2 = int(.1 * height)
Y3 = int(.3 * height)
Y4 = height - Y1 - Y2 - Y3
map_center_x, map_center_y = tile_no_x/2, tile_no_y/2

screen_size = {
    'main': (width, height),
    g.StateID.MAP: {
        'map': (X1, height),
        'player': (X2, Y1),
        'game info': (X2, Y2),
        'messages': (X2, Y3),
        'enemy': (X2, Y4)},
    g.StateID.MAIN_MENU: {
        'menu': (width, height)},
    g.StateID.INVENTORY: {
        'menu': (width*.5, height),
        'details': (width*.5, height)},
    g.StateID.GAME_OVER: {
        'main': (width, height)}}

screen_coordinates = {
    'main': (0, 0),
    g.StateID.MAP: {
        'map': (0, 0),
        'player': (X1, 0),
        'game info': (X1, Y1),
        'messages': (X1, Y2 + Y1),
        'enemy': (X1, Y3 + Y2 + Y1)},
    g.StateID.MAIN_MENU: {
        'menu': (0, 0)},
    g.StateID.INVENTORY: {
        'menu': (0, 0),
        'details': (width*.5, 0)},
    g.StateID.GAME_OVER: {
        'main': (0, 0)}}

# screen names

# Main Screen
MAIN = pygame.display.set_mode(screen_size['main'], 0, 32)