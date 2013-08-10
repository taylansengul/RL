import copy


class Rechargeable(object):
    """
    Pair object consists of two elements (current and capacity) where first element is the current status and the second
    element is the maximum capacity.
    """
    def __init__(self, game, owner=None, current=None, capacity=0):
        self.game = game
        self.owner = owner
        self.capacity = capacity
        self.current_conditions = []
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
        if isinstance(self.current, int):
            return self.current == self.capacity
        elif isinstance(self.current, float):
            return self.current > self.capacity - 0.00001

    def is_zero(self):
        if isinstance(self.current, int):
            return self.current == 0
        elif isinstance(self.current, float):
            return self.current < 0.00001

    def get_time_to_charge(self):
        return self.capacity - self.current

    def add_condition(self, condition):
        # need to make a deepcopy in order to not mutate the properties of a stackable game item
        condition_copy = copy.deepcopy(condition)
        self.current_conditions.append(condition_copy)
        self.game.resource_manager.add_resource(self)

    def remove_condition(self, condition):
        self.current_conditions.remove(condition)
        if not self.current_conditions:
            self.game.resource_manager.remove_resource(self)

    def update(self):
        total_change = 0
        for condition in self.current_conditions:
            total_change += condition['change'][0]
            if condition['type'] != 'permanent':
                condition['change'].pop(0)
        self.change_current(total_change)

        for condition in self.current_conditions:
            if not condition['change']:  # if condition['change'] list is empty
                self.remove_condition(condition)  # remove condition

    def __str__(self):
        return str(self.current) + ' / ' + str(self.capacity)


