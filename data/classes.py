common_player_properties = 'player, can open doors, container, movable, is alive, '
food_needing = {'effects': 'hunger', 'change': [-1], 'type': 'permanent'}

dictionary = {'fighter': {'hp': 10,
                          'attack': 3,
                          'defense': 2,
                          'objects': ['lantern', 'apple'],
                          'properties': common_player_properties,
                          'conditions': [food_needing]}}