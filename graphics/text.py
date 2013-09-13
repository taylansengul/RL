import pygame
from globals import *
import fonts


class Text(object):
    """ A text surface
    """
    def __init__(self, screen=None, context=None, coordinates=None, color=None, font=CONSOLE_FONT,
                 horizontal_align='left', vertical_align='top', anti_alias=False):
        """color can be a string or RGB-tuple"""
        self.screen = screen
        self.context = context
        self.coordinates = coordinates
        self.color = Text.get_color(color)
        self.font = Text.get_font(font)

        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        self.anti_alias = anti_alias

    @staticmethod
    def get_font(font_name):
        fonts_dictionary = {'map object': fonts.MAP_OBJECT,
                            CONSOLE_FONT: fonts.CONSOLE,
                            INVENTORY_FONT: fonts.INVENTORY,
                            MAIN_MENU_FONT: fonts.MAIN_MENU}
        return fonts_dictionary[font_name]

    @staticmethod
    def get_color(color):
        if isinstance(color, str):
            return ColorID[color]
        else:
            return color

    def render(self):
        """renders text to self.screen
        Draw text with the given parameters on the given surface.

        rectOrPosToDrawTo - Where to render the text at.  This can be a 2
        item tuple or a Rect.  If a position tuple is used, the align
        arguments will be ignored.


        alignHoriz - Specifies horizontal alignment of the text in the
        rectOrPosToDrawTo Rect.  If rectOrPosToDrawTo is not a Rect, the
        alignment is ignored.

        alignVert - Specifies vertical alignment of the text in the
        rectOrPosToDrawTo Rect.  If rectOrPosToDrawTo is not a Rect, the
        alignment is ignored.

        antialias - Whether to draw the text anti-aliased or not.
        """
        fontSurface = self.font.render(self.context, self.anti_alias, self.color)
        if isinstance(self.coordinates, tuple):
            self.screen.surface.blit(fontSurface, self.coordinates)
        elif isinstance(self.coordinates, pygame.Rect):
            fontRect = fontSurface.get_rect()
            # align horizontally
            if self.horizontal_align == 'center':
                fontRect.centerx = self.coordinates.centerx
            elif self.horizontal_align == 'right':
                fontRect.right = self.coordinates.right
            else:
                fontRect.x = self.coordinates.x  # left
            # align vertically
            if self.vertical_align == 'center':
                fontRect.centery = self.coordinates.centery
            elif self.vertical_align == 'bottom':
                fontRect.bottom = self.coordinates.bottom
            else:
                fontRect.y = self.coordinates.y  # top

            self.screen.surface.blit(fontSurface, fontRect)
        self.screen.render_to_main()