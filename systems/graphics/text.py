import pygame
from data import fonts


class Text(object):
    def __init__(self, game, screen=None, context=None, coordinates=None, color=None, font='arial', font_size=12,
                 horizontal_align='left', vertical_align='top', anti_alias=False):
        """color can be a string or RGB-tuple"""
        self.game = game
        self.screen = screen
        self.context = context
        self.coordinates = coordinates
        if isinstance(color, str):
            self.color = self.game.data.colors.palette[color]
        else:
            self.color = color
        if font == 'map object':
            self.font = fonts.MAP_OBJECT
        elif font == 'console':
            self.font = fonts.CONSOLE
        else:
            self.font = font

        self.font_size = font_size
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        self.anti_alias = anti_alias

    def render(self):
        """renders text to self.screen"""
        self.draw()
        self.screen.render()

    def draw(self):
        '''
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
        '''
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