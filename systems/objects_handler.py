class Objects_Handler():
    def __init__(self):
        self.player = None
        self.NPCs = []
        self.game_items = []
        self.all_objects = []

    def add_player(self, player):
        self.player = player
        self.all_objects.append(player)

    def add_NPC(self, NPC):
        self.NPCs.append(NPC)
        self.all_objects.append(NPC)

    def add_game_item(self, item_):
        self.game_items.append(item_)
        self.all_objects.append(item_)

    def remove_NPC(self, NPC):
        self.NPCs.remove(NPC)
        self.all_objects.remove(NPC)

    def remove_game_item(self, item_):
        self.game_items.remove(item_)
        self.all_objects.remove(item_)


def main():
    o = Objects_Handler()
    print o.game_items

if __name__ == '__main__':
    main()