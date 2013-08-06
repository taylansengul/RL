from random import choice


class Rectangle(object):
    """ used to generate rooms in the dungeon."""
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def intersect(self, rectangles_list):
        """Returns True if self intersects given list, Returns False if the given list is empty or self does not
        intersect the given list"""
        r1 = self
        if not rectangles_list:  # does not intersect if there are no rectangles to intersect
            return False
        for r2 in rectangles_list:  # if intersects one return True
            if (r2.x <= r1.x <= r2.x + r2.w or r2.x <= r1.x + r1.w <= r2.x + r2.w) and \
                    (r2.y <= r1.y <= r2.y + r2.h or r2.y <= r1.y + r1.h <= r2.y + r2.y):
                return True
        else:  # if intersects none return False
            return False

    def get_center(self):
        """Returns the center of self"""
        x = (self.x + self.w)/2
        y = (self.y + self.h)/2
        return x, y

    def get_random(self):
        """Returns a random coordinate from all points of self"""
        return choice(self.get_all())

    def get_boundary(self):
        """Returns a set of coordinates of boundary of self"""
        boundary = []
        for x in range(self.x, self.x + self.w + 1):
            boundary.append((x, self.y))
            boundary.append((x, self.y + self.h))
        for y in range(self.y, self.y + self.h + 1):
            boundary.append((self.x, y))
            boundary.append((self.x + self.w, y))
        return set(boundary)

    def get_corners(self):
        """Returns a set of coordinates of boundary of self"""
        return {(self.x, self.y), (self.x + self.w, self.y),
                (self.x, self.y + self.h), (self.x + self.w, self.y + self.h)}

    def get_interior(self):
        """Returns coordinates of interior of self"""
        return [c for c in self.get_all() if c not in self.get_boundary()]

    def get_all(self):
        """Returns coordinates of all of self"""
        return [(x, y) for x in range(self.x, self.x + self.w) for y in range(self.y, self.y + self.h)]

    def get_distance(self, other):
        """ returns x1, y1, x2, y2, d where (x1, y1), (x2, y2) are coordinates in room1, room2 resp. with distance d
        and this is closest possible distance between two points belonging to room1 and room2. For aesthetic reason,
        we want these points not to lie on the corners. But this is not possible if the room boundary consists only of
        corner points (ex: room is i*j tiles where i, j = 1, 2)"""
        distance = float('inf')  # infinity
        X1, X2, Y1, Y2 = None, None, None, None

        # reminder: boundary contains corners
        corners1 = self.get_corners()       # corners of room self
        boundary1 = self.get_boundary()     # boundary of room self
        corners2 = other.get_corners()      # corners of room other
        boundary2 = other.get_boundary()    # boundary of room other

        if corners1 == boundary1:  # if room1 boundary consists only of corner points
            search_list1 = boundary1  # search through all the boundary
        else:
            search_list1 = [c for c in boundary1 if c not in corners1]  # search through boundary but not corners
        if corners2 == boundary2:  # same as above
            search_list2 = boundary2
        else:
            search_list2 = [c for c in boundary2 if c not in corners2]

        for x1, y1 in search_list1:
            for x2, y2 in search_list2:
                d = abs(x1 - x2) + abs(y1 - y2)
                if d < distance:
                    X1, X2, Y1, Y2, distance = x1, x2, y1, y2, d
        return X1, Y1, X2, Y2, distance

    def __str__(self):
        return str([self.x, self.y, self.w, self.h])