class Rechargeable(object):
    """
    Pair object consists of two elements (current and capacity) where first element is the current status and the second
    element is the maximum capacity.
    """
    def __init__(self, game, owner=None, current=None, capacity=0):
        self.game = game
        self.owner = owner
        self.capacity = capacity
        self.conditions = []
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

    def add_condition(self, condition):
        self.conditions.append(condition)
        self.game.resource_manager.add_resource(self)

    def remove_condition(self, condition):
        self.conditions.remove(condition)
        self.game.resource_manager.remove_resource(self)

    def update(self):
        for condition in self.conditions:
            self.change_current(condition['change'][0])
            if condition['type'] != 'permanent':
                condition['change'].pop(0)

        for condition in self.conditions:
            if not condition['change']:  # if condition['change'] list is empty
                self.remove_condition(condition)  # remove condition

    def __str__(self):
        return str(self.current) + ' / ' + str(self.capacity)


