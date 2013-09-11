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

from globals import *

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

dictionary = {}
screen_size = {
    ScreenID.MAIN: (width, height),
    StateID.MAP: {
        ScreenID.MAP: (X1, height),
        ScreenID.PLAYER: (X2, Y1),
        ScreenID.GAME_INFO: (X2, Y2),
        ScreenID.MESSAGES: (X2, Y3),
        ScreenID.ENEMY: (X2, Y4)},
    StateID.MAIN_MENU: {
        ScreenID.MAIN_MENU: (width, height)},
    StateID.INVENTORY: {
        ScreenID.INVENTORY_MENU: (width*.5, height),
        ScreenID.INVENTORY_DETAILS: (width*.5, height)},
    StateID.GAME_OVER: {
        ScreenID.MAIN: (width, height)}}

screen_coordinates = {
    ScreenID.MAIN: (0, 0),
    StateID.MAP: {
        ScreenID.MAP: (0, 0),
        ScreenID.PLAYER: (X1, 0),
        ScreenID.GAME_INFO: (X1, Y1),
        ScreenID.MESSAGES: (X1, Y2 + Y1),
        ScreenID.ENEMY: (X1, Y3 + Y2 + Y1)},
    StateID.MAIN_MENU: {
        ScreenID.MAIN_MENU: (0, 0)},
    StateID.INVENTORY: {
        ScreenID.INVENTORY_MENU: (0, 0),
        ScreenID.INVENTORY_DETAILS: (width*.5, 0)},
    StateID.GAME_OVER: {
        ScreenID.MAIN: (0, 0)}}

# screen names

# Main Screen
MAIN = pygame.display.set_mode(screen_size[ScreenID.MAIN], 0, 32)