__author__ = 'Taylan Sengul'


class Condition(object):
    def __init__(self, duration='instant', effect=0, turns=0, ):
        # todo: wears off
        """
        -- duration: string
            -- 'permanent': Permanent
            -- 'instant': Instant
            -- 'every turn': Every Turn
            -- 'wears off': wears off in time
        -- if 'permanent':
            -- effect stays as long as not removed from a resource.
        -- if 'instant':
            -- effects at that instant and removed
        """