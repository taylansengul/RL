class InventoryStateScreenUpdater():
    def __init__(self, game, screens):
        self.game = game
        self.screens = screens

    @property
    def highlighted_item(self):
        return self.game.state_manager.inventory_state.highlighted_item

    @property
    def menu(self):
        return self.game.state_manager.inventory_state.menu

    def run(self):
        self._render_inventory_menu()
        self._render_highlighted_item_description()
        self.game.pygame.display.flip()

    def _render_inventory_menu(self):
        """render inventory menu to """
        self.menu.render()

    def _render_highlighted_item_description(self):
        if not self.highlighted_item:
            return
        screen = self.screens['details']
        self.highlighted_item.render_description_to(screen)