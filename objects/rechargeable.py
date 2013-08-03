class Rechargeable(object):
    """
    Pair object consists of two elements (current and capacity) where first element is the current status and the second
    element is the maximum capacity.
    """
    def __init__(self, current=0, capacity=0):
        self.capacity = capacity
        if current:
            self.current = current
        else:
            self.current = self.capacity

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

    def __str__(self):
        return str(self.current) + ' / ' + str(self.capacity)


