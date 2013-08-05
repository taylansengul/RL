import screens


class Level_Design(object):
    NPCs = [{'race': 'orc', 'number': (5, 10)}, {'race': 'rat', 'number': (10, 15)}]

    game_items = [{'item': 'apple', 'number': (3, 6)}]

    dungeon_level_1 = {'dungeon width': screens.Screens.tile_no_x,
                       'dungeon height': screens.Screens.tile_no_y,
                       'min_room_number': 6,
                       'max_room_number': 10,
                       'min room width': 3,
                       'max room width': 7,
                       'min room height': 3,
                       'max room height': 7}