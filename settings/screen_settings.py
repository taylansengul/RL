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
from enums import *

width = 1200
height = 720
W = width
H = height
tile_length = 32
X1 = int(.7 * W)
tile_no_x = X1 / tile_length
tile_no_y = H / tile_length
X2 = int(.2 * W)

Y1 = int(.3 * H)
Y2 = int(.1 * H)
Y3 = int(.3 * H)
Y4 = H - Y1 - Y2 - Y3
map_center_x, map_center_y = tile_no_x/2, tile_no_y/2

screens = {
    MAIN_SCREEN: dict(state=None,
                          screen=MAIN_SCREEN,
                          top=0,
                          left=0,
                          width=W,
                          height=H,
                          border=0),
    MAP_SCREEN: dict(state=MAP_STATE,
                         screen=MAP_SCREEN,
                         top=0,
                         left=0,
                         width=X1,
                         height=H,
                         border=0),
    PLAYER_SCREEN: dict(state=MAP_STATE,
                            screen=PLAYER_SCREEN,
                            top=0,
                            left=X1,
                            width=W-X1,
                            height=Y1,
                            border=1),
    GAME_INFO_SCREEN: dict(state=MAP_STATE,
                               screen=GAME_INFO_SCREEN,
                               top=Y1,
                               left=X1,
                               width=W-X1,
                               height=Y2,
                               border=1),
    MESSAGES_SCREEN: dict(state=MAP_STATE,
                              screen=MESSAGES_SCREEN,
                              top=Y1+Y2,
                              left=X1,
                              width=W-X1,
                              height=Y3,
                              border=1),
    ENEMY_SCREEN: dict(state=MAP_STATE,
                           screen=ENEMY_SCREEN,
                           top=Y1+Y2+Y3,
                           left=X1,
                           width=W-X1,
                           height=Y4,
                           border=1),
    MAIN_MENU_SCREEN: dict(state=MAIN_MENU_STATE,
                               screen=MAIN_MENU_SCREEN,
                               top=0,
                               left=0,
                               width=W,
                               height=H,
                               border=0),
    INVENTORY_MENU_SCREEN: dict(state=INVENTORY_STATE,
                                    screen=INVENTORY_MENU_SCREEN,
                                    top=0,
                                    left=0,
                                    width=W/2,
                                    height=H,
                                    border=1),
    INVENTORY_DETAILS_SCREEN: dict(state=INVENTORY_STATE,
                                       screen=INVENTORY_DETAILS_SCREEN,
                                       top=0,
                                       left=W/2,
                                       width=W/2,
                                       height=H,
                                       border=1),
    GAME_OVER_SCREEN: dict(state=GAME_OVER_STATE,
                               screen=GAME_OVER_SCREEN,
                               top=0,
                               left=0,
                               width=W,
                               height=H,
                               border=0)}