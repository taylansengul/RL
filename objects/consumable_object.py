from basic_object import Basic_Object
import data


class Consumable_Object(Basic_Object):
    def __init__(self, **kwargs):
        super(Consumable_Object, self).__init__(**kwargs)
        self.effects = kwargs['effects']
        self.isPickable = True


def main():
    kwargs = {'coordinates': (2, 2)}
    kwargs = dict(kwargs.items() + data.Items.dict_['apple'].items())
    if kwargs['type'] == 'consumable':
        apple = Consumable_Object(kwargs)
        print apple

if __name__ == '__main__':
    main()