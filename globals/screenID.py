class ScreenIDObject:
    def __init__(self, name):
        self.name = name


class ScreenID:
    MAIN = ScreenIDObject("MAIN")
    MAP = ScreenIDObject("MAP")
    PLAYER = ScreenIDObject("PLAYER")
    GAME_INFO = ScreenIDObject("GAME_INFO")
    MESSAGES = ScreenIDObject("MESSAGES")
    ENEMY = ScreenIDObject("ENEMY")
    MAIN_MENU = ScreenIDObject("MAIN_MENU")
    INVENTORY_MENU = ScreenIDObject("INVENTORY_MENU")
    INVENTORY_DETAILS = ScreenIDObject("INVENTORY_DETAILS")
    GAME_OVER = ScreenIDObject("GAME_OVER")