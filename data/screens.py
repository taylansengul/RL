class Screens:
    # screen sizes
    width = 1200
    height = 720
    tile_length = 60
    tile_no_x = 16
    tile_no_y = 12

    screen_size = {'main': (20 * tile_length, 12 * tile_length),
                   'map state': {'map': (16 * tile_length, 12 * tile_length),
                                 'player': (.2 * width, 4 * tile_length),
                                 'game info': (.2 * width, 1 * tile_length),
                                 'messages': (.2 * width, 3 * tile_length),
                                 'enemy': (.2 * width, 4 * tile_length)},
                   'main menu state': (16 * tile_length, 12 * tile_length),
                   'inventory state': (16 * tile_length, 12 * tile_length)}

    screen_coordinates = {'main': (0, 0),
                          'map state': {'map': (0, 0),
                                              'player': (.8 * width, 0),
                                              'game info': (.8 * width, 4 * tile_length),
                                              'messages': (.8 * width, 5 * tile_length),
                                              'enemy': (.8 * width, 8 * tile_length)},
                          'main menu state': (0, 0),
                          'inventory state': (0, 0)}