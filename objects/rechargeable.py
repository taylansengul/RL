class Rechargeable(object):
    """
    Pair object consists of two elements (current and capacity) where first element is the current status and the second
    element is the maximum capacity.
    """
    def __init__(self, game, owner=None, current=None, capacity=0):
        self.game = game
        self.owner = owner
        self.capacity = capacity
        self.change_over_time = []
        if current is None:
            self.current = self.capacity
        else:
            self.current = current

    def change_current(self, amount):
        if amount >= 0:
            self.current = min(self.current + amount, self.capacity)
        else:
            self.current = max(self.current + amount, 0)

    def change_capacity(self, x):
        self.capacity += x

    def full_discharge(self):
        self.current = 0

    def make_full(self):
        self.current = self.capacity

    def make_empty(self):
        return self.current

    def is_full(self):
        return self.current == self.capacity

    def is_zero(self):
        return self.current == 0

    def get_time_to_charge(self):
        return self.capacity - self.current

    def add_to_change_list(self, a_list):
        self.change_over_time += a_list
        self.game.resource_manager.add_to_update_list(self)

    def update(self):
        if self.change_over_time:
            self.change_current(self.change_over_time[0])
            self.change_over_time.pop(0)
        if not self.change_over_time:
            pass


    def __str__(self):
        return str(self.current) + ' / ' + str(self.capacity)


