# CONDITIONS
food_needing = {'effects': 'hunger', 'change': [-1], 'type': 'permanent'}
regeneration = {'effects': 'hp', 'change': [.1], 'type': 'permanent'}
initial_poison = {'effects': 'hp', 'change': [-.3]*8, 'type': 'temporary'}

# PROPERTIES
common_player_properties = 'player, can open doors, container, movable, alive, has vision, needs food, drawable'
# COMMON SETTINGS
player_settings = {'icon': '@', 'color': 'red', 'ID': 'player'}

dictionary = {
    'fighter': {
        'hp': 4,
        'attack': 3,
        'defense': 2,
        'visibility radius': 2,
        'inventory': ['binoculars', 'apple'],
        'hunger': 100,
        'properties': common_player_properties,
        'conditions': [food_needing, regeneration, initial_poison]}}