# CONDITIONS
food_needing = {
    'resource': 'hunger',
    'change': [-1],
    'duration': 'every turn'}
regeneration = {'resource': 'hp', 'change': [.1], 'duration': 'every turn'}
initial_poison = {'resource': 'hp', 'change': [-.3]*8, 'duration': 'temporary'}

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