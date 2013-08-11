common_player_properties = 'player, can open doors, container, movable, is alive, '
food_needing = {'effects': 'hunger', 'change': [-1], 'type': 'permanent'}
regeneration = {'effects': 'hp', 'change': [.1], 'type': 'permanent'}
initial_poison = {'effects': 'hp', 'change': [-2, -1, -1], 'type': 'temporary'}

dictionary = {'fighter': {'hp': 10,
                          'attack': 3,
                          'defense': 2,
                          'visibility radius': 2,
                          'objects': ['lantern', 'apple'],
                          'properties': common_player_properties,
                          'conditions': [food_needing, regeneration, initial_poison]}}