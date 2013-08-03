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