from entities.entity import Entity
from systems.resource_manager import ResourceManager


class Ticker(object):
    """
    Simple timer for roguelike games.
    From:
    A simple turn scheduling system -- Python implementation
    http://www.roguebasin.roguelikedevelopment.org
    """
    ticks = 0  # current ticks--sys.maxint is 2147483647
    schedule = {}  # this is the dict of things to do {ticks: [obj1, obj2, ...], ticks+1: [...], ...}

    @staticmethod
    def register(interval, obj):
        """
        an object has to register to Ticker to be processed.
        """
        time = Ticker.ticks + interval
        Ticker.schedule.setdefault(time, []).append(obj)
        # setdefault: return the value if time is in Ticker.schedule otherwise return [].

    @staticmethod
    def get_tick(obj):
        for tick in Ticker.schedule:
            if obj in Ticker.schedule[tick]:
                return tick
        else:
            return None

    @staticmethod
    def deregister(obj):
        turn = Ticker.get_tick(obj)
        if turn:
            Ticker.schedule[turn].remove(obj)

    @staticmethod
    def next_turn():
        things_to_do = Ticker.schedule.pop(Ticker.ticks, [])
        for obj in things_to_do:
            obj.do_turn()


class Time(object):
    turn = 1

    @staticmethod
    def new_turn():
        messages = []
        # run resource manager
        ResourceManager.manage()
        # update NPC status
        for NPC in Entity.all_NPCs:
            message, __ = NPC.update_status()
            messages.append(message)
        # update player status
        game_over_message, game_over = Entity.player.update_status()

        # player vision changes
        Entity.player.update_vision()
        # todo: ai action
        Time.turn += 1
        return messages, game_over, game_over_message
