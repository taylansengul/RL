import random


def random_choose(a_list):
    """ returns an event according to probabilities """
    # a_list = [{"event": "given_event", "probability": "given_probability"},...]
    probabilities = [el['probability'] for el in a_list]
    events = [el['event'] for el in a_list]
    cdf = [sum(j for j in probabilities[:k]) for k in range(len(a_list))]
    r = random.random()
    R = max([j for j,p in enumerate(cdf) if p <= r])
    return events[R]

def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points