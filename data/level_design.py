from random import randint


class Level_Design(object):
    NPCs = [{'item': 'orc', 'coordinates': (2, 2)}]

    game_items = [{'item': 'apple', 'coordinates': (2, 1)}]

    dungeon_level_1 = {'dungeon width': 16,
                       'dungeon height': 12,
                       'min_room_number': 5,
                       'max_room_number': 8,
                       'min room width': 3,
                       'max room width': 5,
                       'min room height': 3,
                       'max room height': 6}