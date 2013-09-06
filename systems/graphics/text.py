class Text(object):
    def __init__(self, game, screen=None, context=None, coordinates=None, color=None, font='arial', font_size=12):
        """color can be a string or RGB-tuple"""
        self.game = game
        self.screen = screen
        self.context = context
        self.coordinates = coordinates
        if isinstance(color, str):
            self.color = self.game.data.colors.palette[color]
        else:
            self.color = color
        self.font = font
        self.font_size = font_size

    def render(self):
        """renders text to self.screen"""
        self.game.font_manager.Draw(self.screen.surface, self.font, self.font_size, self.context, self.coordinates,
                                    self.color, 'left', 'top', True)
        self.screen.render()

    def draw(self, rectOrPosToDrawTo,
            alignHoriz='left', alignVert='top', antialias=False):
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
        fontSurface = self.font.render(self.context, antialias, self.color)
        if isinstance(rectOrPosToDrawTo, tuple):
            self.screen.surface.blit(fontSurface, rectOrPosToDrawTo)
        elif isinstance(rectOrPosToDrawTo, pygame.Rect):
            fontRect = fontSurface.get_rect()
            # align horiz
            if alignHoriz == 'center':
                fontRect.centerx = rectOrPosToDrawTo.centerx
            elif alignHoriz == 'right':
                fontRect.right = rectOrPosToDrawTo.right
            else:
                fontRect.x = rectOrPosToDrawTo.x  # left
            # align vert
            if alignVert == 'center':
                fontRect.centery = rectOrPosToDrawTo.centery
            elif alignVert == 'bottom':
                fontRect.bottom = rectOrPosToDrawTo.bottom
            else:
                fontRect.y = rectOrPosToDrawTo.y  # top

            self.screen.surface.blit(fontSurface, fontRect)