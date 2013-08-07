common_player_properties = 'player, can open doors, container, movable, is alive, '

dictionary = {'fighter': {'hp': 10,
                          'attack': 3,
                          'defense': 2,
                          'objects': ['lantern', 'apple'],
                          'properties': common_player_properties,
                          'conditions': 'poisoned({"turn":3, "damage":1})'}}
