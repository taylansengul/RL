import screens

NPCs = [{'race': 'orc', 'number': (5, 10)}, {'race': 'rat', 'number': (10, 15)}]

game_items = [{'item': 'apple', 'number': (5, 8)}, {'item': 'potion of healing', 'number': (5, 8)}]

dungeon_level_1 = {'dungeon width': screens.tile_no_x,
                   'dungeon height': screens.tile_no_y,
                   'min_room_number': 6,
                   'max_room_number': 10,
                   'min room width': 3,
                   'max room width': 7,
                   'min room height': 3,
                   'max room height': 7}