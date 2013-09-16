import copy
from systems.resource_manager import ResourceManager


class Resource(object):
    """
    Pair object consists of two elements (current and maximum) where first element is the current status and the second
    element is the maximum maximum.
    """
    def __init__(self, owner=None, minimum=0, current=None, maximum=0):
        self.owner = owner
        self.minimum = minimum
        self.maximum = maximum
        self.current_conditions = []
        if current is None:
            self.current = self.maximum
        else:
            self.current = current

    def change_current(self, amount):
        if amount >= 0:
            self.current = min(self.current + amount, self.maximum)
        else:
            self.current = max(self.current + amount, self.minimum)

    def is_zero(self):
        if isinstance(self.current, int):
            return self.current == 0
        elif isinstance(self.current, float):
            return self.current < 0.00001

    def add_condition(self, condition):
        # need to make a deepcopy in order to not mutate the properties of a stackable game item
        condition_copy = copy.deepcopy(condition)
        self.current_conditions.append(condition_copy)
        ResourceManager.add_resource(self)

    def remove_condition(self, condition):
        self.current_conditions.remove(condition)
        if not self.current_conditions:
            ResourceManager.remove_resource(self)

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
        return str(self.current) + ' / ' + str(self.maximum)