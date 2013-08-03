from tile import Tile
from random import randint


class Dungeon(object):
    def __init__(self, **kwargs):
        self.rooms = []
        self.min_room_number = kwargs['min_room_number']
        self.max_room_number = kwargs['max_room_number']
        self.min_room_width = kwargs['min room width']
        self.max_room_width = kwargs['max room width']
        self.min_room_height = kwargs['min room height']
        self.max_room_height = kwargs['max room height']
        self.dungeon_width = kwargs['dungeon width']
        self.dungeon_height = kwargs['dungeon height']
        self.map2D_tip = [[None for _ in range(self.dungeon_height)] for _ in range(self.dungeon_width)]
        self.map2D = [[None for _ in range(self.dungeon_height)] for _ in range(self.dungeon_width)]

        # number of rooms
        self.room_number = randint(self.min_room_number, self.max_room_number)

        # create dungeon
        self.create_dungeon()

    def carve_room(self, rectangle):
        for m in range(rectangle.x, rectangle.x + rectangle.w):
            for n in range(rectangle.y, rectangle.y + rectangle.h):
                self.map2D_tip[m][n] = 'floor'

    def carve_tunnel(self, (x1, y1), (x2, y2), method='horizontal first'):
        if method == 'horizontal first':
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.map2D_tip[x][y1] == 'floor'
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.map2D_tip[x2][y] == 'floor'

    def carve_all_rooms(self):
        for room in range(self.room_number):
            w = randint(self.min_room_width, self.max_room_width)
            h = randint(self.min_room_height, self.max_room_height)
            x = randint(0, self.dungeon_width - w)
            y = randint(0, self.dungeon_height - h)
            new_room = Rectangle(x, y, w, h)
            failed = False
            if len(self.rooms) == 0:
                pass
            else:
                for other_room in self.rooms:
                    if new_room.intersect(other_room):
                        failed = True
                        break
            if failed:
                pass
            else:
                self.rooms.append(new_room)
                self.carve_room(new_room)




    def create_dungeon(self):
        # initialize map2D with walls everywhere
        for m in range(self.dungeon_width):
            for n in range(self.dungeon_height):
                self.map2D_tip[m][n] = 'wall'

        self.carve_all_rooms()

        for m in range(self.dungeon_width):
            for n in range(self.dungeon_height):
                self.map2D[m][n] = Tile(coordinates=(m, n), tip=self.map2D_tip[m][n])

        print len(self.rooms)
        self.player_starting_coordinates = self.rooms[0].get_center()


class Rectangle(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def intersect(self, other):
        r1 = self
        r2 = other
        if ((r2.x <= r1.x <= r2.x + r2.w) or (r2.x <= r1.x + r1.w <= r2.x + r2.w)) and \
            ((r2.y <= r1.y + r1.h <= r2.y + r2.h) or (r2.y <= r1.y + r1.h <= r2.y + r2.y)):
            return True
        else:
            return False

    def get_center(self):
        x = (self.x + self.w)/2
        y = (self.y + self.h)/2
        return x, y

if __name__ == '__main__':
    dungeon_level_1 = {'dungeon width': 100,
                       'dungeon height': 100,
                       'min_room_number': 4,
                       'max_room_number': 10,
                       'min room width': 4,
                       'max room width': 6,
                       'min room height': 5,
                       'max room height': 9}
    d = Dungeon(**dungeon_level_1)
