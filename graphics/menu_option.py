class Menu_Option:
    def __init__(self, text, pos, font, isHovered=False):
        self.font = font
        self.text = text
        self.pos = pos
        self.isHovered = isHovered
        self.rend = None
        self.set_rend()
        self.rect = None
        self.set_rect()

    def draw(self, screen):
        self.set_rend()
        screen.surface.blit(self.rend, self.rect)

    def set_rend(self):
        if self.isHovered:
            color = (255, 255, 255)
        else:
            color = (100, 100, 100)
        self.rend = self.font.render(self.text, True, color)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos