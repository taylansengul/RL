import copy
from systems.resource_manager import ResourceManager
# from systems.time import Ticker


class Resource(object):
    """
    A resource used to represent hitpoints, mana or similar attributes which have a minimum, current and maximum.
    """
    def __init__(self, minimum=0, current=None, maximum=0):
        self.minimum = minimum
        self.maximum = maximum
        self.current_conditions = []
        if current is None:
            self.current = self.maximum
        else:
            self.current = current
        assert self.minimum <= self.current <= self.maximum

    def change_current(self, amount):
        if amount >= 0:
            self.current = min(self.current + amount, self.maximum)
        else:
            self.current = self.current + amount

    def less_than_minimum(self):
        return self.current <= self.minimum

    def add_condition(self, condition):
        # todo: wears off
        """
        condition has
        -- duration: string
            -- 'permanent': Permanent
            -- 'instant': Instant
            -- 'wears off': wears off in time
        -- if 'permanent':
            -- effect stays as long as not removed from a resource.
        -- if 'instant':
            -- effects at that instant and removed
        """
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
            if condition['duration'] != 'every turn':
                condition['change'].pop(0)
        self.change_current(total_change)

        for condition in self.current_conditions:
            if not condition['change']:  # if condition['change'] list is empty
                self.remove_condition(condition)  # remove condition

    def __str__(self):
        return str(self.current) + ' / ' + str(self.maximum)