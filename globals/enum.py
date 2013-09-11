class EnumMeta(type):
    """http://tech.zarmory.com/2013/08/python-enum-on-steroids.html"""
    __excludes__ = ()

    def __new__(mcs, name, base, d):
        cls = super(EnumMeta, mcs).__new__(mcs, name, base, d)
        cls.__values__ = set()
        cls.__members__ = dict()
        for k, v in cls.__dict__.items():
            if k in cls.__excludes__ or k.startswith("_") or k.find("__") > 0:
                continue

            pname = getattr(cls, k+"__name", k)
            pdesc = getattr(cls, k+"__desc", "")
            prop = type(type(v).__name__, (type(v),), {"name" : pname, "desc" : pdesc})
            p = prop(v)
            setattr(cls, k, p)
            cls.__values__.add(p)
            cls.__members__[v] = p

        return cls

    def __contains__(self, val):
        return val in self.__values__

    def __iter__(self):
        for i in self.__values__:
            yield i

    def __len__(self):
        return len(self.__values__)

    def __by_name__(self, name):
        if not hasattr(self, name):
            raise ValueError("%s has no property named %s" % (self.__name__, name))
        return getattr(self, name)

    def __call__(self, val):
        if val not in self.__members__:
            raise ValueError("%s has no property with value %s" % (self.__name__, val))
        return self.__members__[val]
                   
                   
class Enum(object):       
    __metaclass__ = EnumMeta  