from tile import Tile
from random import randint, choice
from rectangle import Rectangle
from entity import Entity


class Dungeon(object):
    def __init__(self, kwargs):
        self.rooms = []
        self.room_number = 0  # to be set in self.create._dungeon
        self.min_room_number = kwargs['min_room_number']
        self.max_room_number = kwargs['max_room_number']
        self.min_room_width = kwargs['min room width']
        self.max_room_width = kwargs['max room width']
        self.min_room_height = kwargs['min room height']
        self.max_room_height = kwargs['max room height']
        self.dungeon_width = kwargs['dungeon width']
        self.dungeon_height = kwargs['dungeon height']
        self.pre_map2D = [[None for _ in range(self.dungeon_height)] for _ in range(self.dungeon_width)]
        self.map2D = [[None for _ in range(self.dungeon_height)] for _ in range(self.dungeon_width)]

    def _add_room(self, rectangle):
        """ 1. Make each coordinate of the pre map which coincide with those given in rectangle a floor tile
            2. Add the rectangle to dungeon rooms"""
        for c in rectangle.get_all():  # gets every coordinate in the rectangle
            self.pre_map2D[c[0]][c[1]] = 'floor'
        self.rooms.append(rectangle)

    def _build_random_room(self):
        """Get a random room, if it does not intersect other rooms inside the dungeon, add it to dungeon rooms"""
        def get_random_rectangle():
            """returns a random rectangle inside the dungeon grid which has distance >= 1 from the borders"""
            w = randint(self.min_room_width, self.max_room_width)
            h = randint(self.min_room_height, self.max_room_height)
            # do not put it next to the dungeon borders
            x = randint(1, self.dungeon_width - w - 2)
            y = randint(1, self.dungeon_height - h - 2)
            return Rectangle(x, y, w, h)

        # get a random rectangle
        new_room = get_random_rectangle()
        # add it to dungeon rooms if it does not intersect existing rooms in the dungeon
        if not new_room.intersect(self.rooms):
            self._add_room(new_room)

    def _build_walls(self):
        """Convert dirt tiles neighboring floor tiles to wall tiles"""

        for m in range(0, self.dungeon_width):
            for n in range(0, self.dungeon_height):
                if self.pre_map2D[m][n] == 'floor':  # if tile is floor
                    for c in self.get_neighboring_coordinates((m, n), 1, self_included=False):  # look for its neighbors
                        x, y = c
                        if self.pre_map2D[x][y] == 'dirt':  # if there is a dirt tile as its neighbor
                            self.pre_map2D[x][y] = 'wall'  # make it a wall tile.

    def _connect_rooms(self):
        """ first connect every room to the closest one, then connect the unconnected components"""

        def find_component(room):
            """ return the component if room belongs to one, otherwise return False."""
            try:  # if the room belongs to a component
                return [component for component in connected_components if room in component][0]
            except IndexError:  # otherwise
                return False

        def carve_tunnel(x1, y1, x2, y2):
            """ connect (x1, y1) with (x2, y2) by floor tiles."""
            if x2 < x1:  # make sure x1 < x2
                x1, y1, x2, y2 = x2, y2, x1, y1

            tunnel = [(m, y1) for m in range(x1, x2)] + [(x2, n) for n in range(min(y1, y2), max(y1, y2) + 1)]
            for x, y in tunnel:
                self.pre_map2D[x][y] = 'floor'

        unconnected_rooms = list(self.rooms)  # initially all rooms are unconnected
        connected_components = []  # initially there is no connected component
        for room1 in unconnected_rooms:
            # connect every room to the closest one
            x1, y1, x2, y2, d, room2 = self._get_closest_room(room1)

            # put the connected rooms into the same component
            carve_tunnel(x1, y1, x2, y2)
            comp1 = find_component(room1)
            comp2 = find_component(room2)
            if not comp1 and not comp2:  # if room1, room2 do not belong to any component
                connected_components.append({room1, room2})  # put them into same component
            elif comp1 and not comp2:  # if room1 belongs to a component but not room2
                comp1.add(room2)  # put room2 into the component of room1
            elif not comp1 and comp2:  # similar
                comp2.add(room1)
            elif comp1 and comp2 and comp1 != comp2:  # if both rooms belong to different components
                connected_components.remove(comp2)  # remove the second component
                comp1.union(comp2)  # merge components
            assert None not in connected_components

        # Finally if there are unconnected components, connect them.
        if len(connected_components) > 1:  # there are unconnected components
            still_unconnected_rooms = []
            for component in connected_components:  # from each unconnected component
                still_unconnected_rooms.append(choice(list(component)))  # pick a random room

            for j, room in enumerate(still_unconnected_rooms):  # for each room in still unconnected rooms
                if j != len(still_unconnected_rooms) - 1:  # except the last one
                    other = still_unconnected_rooms[j + 1]
                    x1, y1, x2, y2 = room.x, room.y, other.x, other.y
                    carve_tunnel(x1, y1, x2, y2)  # connect it with the next room in the unconnected rooms list

    def _get_closest_room(self, room):
        """Returns X1, Y1, X2, Y2, distance, closest_room
        X1, Y1 coordinates in current room
        X2, Y2 coordinates in the closest room
        distance = Manhattan distance between these two coordinates
        """
        distance = float('inf')  # set the distance to infinity
        X1, Y1, X2, Y2, closest_room = None, None, None, None, None  # initialize
        for another_room in self.rooms:
            x1, y1, x2, y2, d = room.get_distance(another_room)
            # print 'x1 =', x1, 'x2 =', x2, 'y1 =', y1, 'y2 =', y2
            if 0 < d < distance:  # ignore the room itself by ignoring d = 0
                X1, Y1, X2, Y2, distance, closest_room = x1, y1, x2, y2, d, another_room

        # print X1, Y1, X2, Y2, closest_room
        # assert X1 is not None and Y1 is not None and X2 is not None and Y2 is not None and closest_room is not None

        return X1, Y1, X2, Y2, distance, closest_room

    def _set_map_from_pre_map(self):
        """Transfer from self.pre_map2D to self.map2D"""
        for m in range(0, self.dungeon_width):
            for n in range(0, self.dungeon_height):
                self.map2D[m][n] = Tile(coordinates=(m, n), tip=self.pre_map2D[m][n])

    def get_neighboring_coordinates(self, center, radius=1, self_included=True):
        """Returns coordinates which are neighbors of given x, y and lies in the dungeon grid"""
        coordinates = []
        x, y = center
        x_left = max(x-radius, 0)
        x_right = min(x+radius, self.dungeon_width)
        y_top = max(y-radius, 0)
        y_bottom = min(y+radius, self.dungeon_height)
        for m in range(x_left, x_right+1):
            for n in range(y_top, y_bottom+1):
                coordinates.append((m, n))
        if not self_included:
            coordinates.remove((x, y))
        return coordinates

    def get_neighboring_tiles(self, tile, radius=1, self_included=True):
        """Returns tiles which are in a neighborhood of given radius and given tile and lies in the dungeon grid
        :rtype : List of Tile Objects
        :param tile: Tile
        :param radius: Integer
        :param self_included: Boolean,
        """
        neighboring_coordinates = self.get_neighboring_coordinates(tile.coordinates, radius, self_included)
        return self.get_tiles(*neighboring_coordinates)

    def get_tiles(self, *coordinates):
        """

        :param coordinates:
        :return:
        """
        tiles = []
        for c in coordinates:
            x, y = c
            try:
                tiles.append(self.map2D[x][y])
            except IndexError:
                pass
        return tiles

    def get_neighbor_tile(self, tile, direction):
        direction_dictionary = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        x1, y1 = tile.coordinates
        x2, y2 = direction_dictionary[direction]
        x, y = x1 + x2, y1 + y2
        if 0 <= x <= self.dungeon_width and 0 <= y <= self.dungeon_height:
            return self.map2D[x][y]

    def get_random_room_floor_tile_with_no_objects(self):
        tile = None
        while True:
            the_random_room = choice(self.rooms)
            coordinates_of_all_tiles_in_the_random_room = the_random_room.get_all()
            m, n = choice(coordinates_of_all_tiles_in_the_random_room)
            tile = self.map2D[m][n]
            if tile.container.is_empty():
                    break
        return tile

    def create_map(self):
        """Populate dungeon with rooms, connecting tunnels and starting place"""
        # initialize map2D with dirt everywhere
        for m in range(self.dungeon_width):
            for n in range(self.dungeon_height):
                self.pre_map2D[m][n] = 'dirt'

        # set a random number of rooms
        self.room_number = randint(self.min_room_number, self.max_room_number)

        # build rooms
        print 'building rooms...',
        co = 0
        while len(self.rooms) < self.room_number and co < 10000:  # build rooms until enough rooms or enough tries
            co += 1
            self._build_random_room()
        print 'done.'

        # connect the rooms by tunnels
        print 'connecting rooms...',
        self._connect_rooms()
        print 'done.'

        # build walls: Convert dirt tiles neighboring floor tiles to wall tiles
        print 'building walls...',
        self._build_walls()
        print 'done.'

        # set the player starting coordinates
        print 'setting player starting coordinates...',
        m, n = self.rooms[0].get_random()
        self.pre_map2D[m][n] = 'entrance'
        self.player_starting_coordinates = (m, n)
        print 'done.'

        # set the exit coordinates
        print 'setting the dungeon exit coordinates...',
        m, n = self.player_starting_coordinates
        possible_exits = []
        for room in self.rooms:  # append all coordinates in all rooms in to possible_exits
            possible_exits.extend(room.get_all())
        # sort possible_exits with respect to their distance from the entrance
        possible_exits = sorted(possible_exits, key=lambda (x, y): (abs(x - m) + abs(y - n)), reverse=True)
        # choose one from the last 10 farthest coordinates
        m1, n1 = choice(possible_exits[:10])
        self.pre_map2D[m1][n1] = 'exit'
        print 'done.'

        # set tiles from tile tips
        print 'setting dungeon map...',
        self._set_map_from_pre_map()
        print 'done.'

    def set_all_tiles_non_visible(self):
        """sets the visibility attribute of all tiles in the dungeon to False"""
        for m in range(self.dungeon_width):
            for n in range(self.dungeon_height):
                self.map2D[m][n].set_visibility(False)