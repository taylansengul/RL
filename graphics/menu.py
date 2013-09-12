from graphics.text import Text
import globals as g


class Menu(list):
    def __init__(self, screen=None, options=None, font=g.FontID.CONSOLE, empty_menu_message='Empty Menu',
                 line_height=18, left_padding=12, top_padding=12):
        super(Menu, self).__init__(options)
        self.screen = screen
        self.highlighted_option_index = 0
        self.highlighted_option_color = 'yellow'
        self.normal_option_color = 'white'
        self.font = font
        self.empty_menu_message = empty_menu_message
        self.line_height = line_height
        self.left_padding = left_padding
        self.top_padding = top_padding

    @property
    def highlighted_option(self):
        return self[self.highlighted_option_index]

    def set_highlighted_option_index(self, new_index):
        """
        sets the highlighted option index to new_index if

        Inputs:
        new_index -- int new index
        """
        self.highlighted_option_index = new_index % len(self)

    def render(self):
        self.screen.clear()
        if len(self) == 0:
            t = Text(
                screen=self.screen,
                context=self.empty_menu_message,
                coordinates=(self.left_padding, self.top_padding),
                color=self.normal_option_color,
                font=self.font)
            t.render()

        for j, option in enumerate(self):
            color = [self.normal_option_color, self.highlighted_option_color][j == self.highlighted_option_index]
            t = Text(
                screen=self.screen,
                context=option,
                coordinates=(self.left_padding, j*self.line_height + self.top_padding),
                color=color,
                font=self.font)
            t.render()
        self.screen.render_to_main()

    def next(self):
        self.set_highlighted_option_index(self.highlighted_option_index+1)

    def prev(self):
        """highlight the previous item on the menu"""
        self.set_highlighted_option_index(self.highlighted_option_index-1)