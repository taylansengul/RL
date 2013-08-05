# screen sizes
width = 1200
height = 720
tile_length = 30
left_bar_width = 8 * width / 10
left_bar_height = height
tile_no_x = left_bar_width / tile_length
tile_no_y = left_bar_height / tile_length
right_bar_width = .2 * width
right_bar_height = height
main_multiplier_x = width / tile_length
main_multiplier_y = height / tile_length
map_multiplier_x = left_bar_width / tile_length
map_multiplier_y = left_bar_height / tile_length
player_height = 3 * height / 10
game_info_height = height / 10
messages_height = 3 * height / 10
enemy_height = 3 * height / 10

screen_size = {'main': (main_multiplier_x * tile_length, main_multiplier_y * tile_length),
               'map state': {'map': (map_multiplier_x * tile_length, map_multiplier_y * tile_length),
                             'player': (right_bar_width, player_height),
                             'game info': (right_bar_width, game_info_height),
                             'messages': (right_bar_width, messages_height),
                             'enemy': (right_bar_width, enemy_height)},
               'main menu state': (16 * tile_length, 12 * tile_length),
               'inventory state': (16 * tile_length, 12 * tile_length)}

screen_coordinates = {'main': (0, 0),
                      'map state': {'map': (0, 0),
                                    'player': (left_bar_width, 0),
                                    'game info': (left_bar_width, player_height),
                                    'messages': (left_bar_width, game_info_height + player_height),
                                    'enemy': (left_bar_width, messages_height + game_info_height + player_height)},
                      'main menu state': (0, 0),
                      'inventory state': (0, 0)}
