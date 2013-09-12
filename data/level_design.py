from settings import screen_settings

NPCs = [{'id': 'orc', 'number': (5, 10)}, {'id': 'rat', 'number': (10, 15)}]

game_items = [{'id': 'apple', 'number': (5, 8)},
              {'id': 'small medkit', 'number': (5, 8)},
              {'id': 'large medkit', 'number': (2, 3)}]

dungeon_level_1 = {'dungeon width': screen_settings.tile_no_x,
                   'dungeon height': screen_settings.tile_no_y,
                   'min_room_number': 60,
                   'max_room_number': 100,
                   'min room width': 1,
                   'max room width': 2,
                   'min room height': 1,
                   'max room height': 2}

# todo: assert that there is enough room in the dungeon for all the game items.