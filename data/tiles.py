__author__ = 'Taylan Sengul'

# todo: walkable tiles.
floor_properties = 'tile, drawable, container'
wall_properties = 'tile, drawable, movement blocking, light blocking'
tiles = {
    '': {
        'icon': '',
        'color': 'white'},
    'wall': {
        'icon': '#',
        'color': 'red',
        'properties': wall_properties},
    'entrance': {
        'icon': '>',
        'color': 'yellow',
        'properties': floor_properties},
    'exit': {
        'icon': '<',
        'color':
            'yellow',
        'properties': floor_properties},
    'floor': {
        'icon': ' ',
        'color': 'blue',
        'properties': floor_properties,
        'image': "floor_tile.png"},
    'open door': {
        'icon': '-',
        'color': 'red'},
    'closed door': {
        'icon': '+',
        'color': 'red'},
    'dirt': {
        'icon': ' ',
        'color': 'black',
        'properties': wall_properties}}