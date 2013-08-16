class Menu(object):
    def __init__(self, screen=None, options=None):
        self.options = options
        self.screen = screen
        self.option_selected = None

    def draw(self):
        # todo: get rid of this fill
        self.screen.fill((0, 0, 0))
        for option in self.options:
            option.draw(self.screen)

    def select_next(self):
        for no, option in enumerate(self.options):
            if option.isHovered:
                option.isHovered = False
                if no == len(self.options) - 1:
                    self.options[0].isHovered = True
                else:
                    self.options[no+1].isHovered = True
                break

    def select_prev(self):
        for no, option in enumerate(self.options):
            if option.isHovered:
                option.isHovered = False
                if no == 0:
                    self.options[len(self.options) - 1].isHovered = True
                else:
                    self.options[no-1].isHovered = True
                break

    def get_active_option(self):
        for option in self.options:
            if option.isHovered:
                return option
        else:  # if there are no options
            return None


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
        screen.blit(self.rend, self.rect)

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


