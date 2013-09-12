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
import globals as g

width = 1200
height = 720
W = width
H = height
tile_length = 32
X1 = int(.8 * W)
tile_no_x = X1 / tile_length
tile_no_y = H / tile_length
X2 = int(.2 * W)

Y1 = int(.3 * H)
Y2 = int(.1 * H)
Y3 = int(.3 * H)
Y4 = H - Y1 - Y2 - Y3
map_center_x, map_center_y = tile_no_x/2, tile_no_y/2

screens = {
    g.ScreenID.MAIN: dict(state=None,
                          screen=g.ScreenID.MAIN,
                          top=0,
                          left=0,
                          width=W,
                          height=H,
                          border=0),
    g.ScreenID.MAP: dict(state=g.StateID.MAP,
                         screen=g.ScreenID.MAP,
                         top=0,
                         left=0,
                         width=X1,
                         height=H,
                         border=0),
    g.ScreenID.PLAYER: dict(state=g.StateID.MAP,
                            screen=g.ScreenID.PLAYER,
                            top=0,
                            left=X1,
                            width=W-X1,
                            height=Y1,
                            border=1),
    g.ScreenID.GAME_INFO: dict(state=g.StateID.MAP,
                               screen=g.ScreenID.GAME_INFO,
                               top=Y1,
                               left=X1,
                               width=W-X1,
                               height=Y2,
                               border=1),
    g.ScreenID.MESSAGES: dict(state=g.StateID.MAP,
                              screen=g.ScreenID.MESSAGES,
                              top=Y1+Y2,
                              left=X1,
                              width=W-X1,
                              height=Y3,
                              border=1),
    g.ScreenID.ENEMY: dict(state=g.StateID.MAP,
                           screen=g.ScreenID.ENEMY,
                           top=Y1+Y2+Y3,
                           left=X1,
                           width=W-X1,
                           height=Y4,
                           border=1),
    g.ScreenID.MAIN_MENU: dict(state=g.StateID.MAIN_MENU,
                               screen=g.ScreenID.MAIN_MENU,
                               top=0,
                               left=0,
                               width=W,
                               height=H,
                               border=0),
    g.ScreenID.INVENTORY_MENU: dict(state=g.StateID.INVENTORY,
                                    screen=g.ScreenID.INVENTORY_MENU,
                                    top=0,
                                    left=0,
                                    width=W/2,
                                    height=H,
                                    border=1),
    g.ScreenID.INVENTORY_DETAILS: dict(state=g.StateID.INVENTORY,
                                       screen=g.ScreenID.INVENTORY_DETAILS,
                                       top=0,
                                       left=W/2,
                                       width=W/2,
                                       height=H,
                                       border=1),
    g.ScreenID.GAME_OVER: dict(state=g.StateID.GAME_OVER,
                               screen=g.ScreenID.GAME_OVER,
                               top=0,
                               left=0,
                               width=W,
                               height=H,
                               border=0)}