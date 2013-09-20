__author__ = 'Taylan Sengul'
from screen import Screen
import settings


class Screens:
    screens = {}

    @staticmethod
    def _initialize_screens():
        D = settings.screen_settings.screens
        for a_screen_ID in D:
            if a_screen_ID == 'MAIN_SCREEN':
                continue
            else:
                Screens.screens[a_screen_ID] = Screen(**D[a_screen_ID])