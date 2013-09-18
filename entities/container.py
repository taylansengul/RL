__author__ = 'Taylan Sengul'


class Container(list):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

    def get(self, **kwargs):
        """
        Return entities found in self satisfying the keywords given.
        if no keywords given, return self
        if key is 1, '1' or not given return first of the found entities.
        if key is 'all' return all of the found entities.
        usage:
        -- container.get(ID='apple'})
        -- container.get(properties='red', properties='red edible'})
        -- container.get(properties='red', properties='red', key='all'})
        """
        # todo: shallow and deep search: an thing can be inside a container which is inside another container
        if kwargs is None:
            return self
        return_list = []
        key = kwargs.pop('key', None)
        for entity in self:
            for search_attr in kwargs:
                entity_attr = getattr(entity, search_attr, None)
                if not (entity_attr and kwargs[search_attr] in entity_attr):
                    break
            else:
                return_list.append(entity)
        if key == 'all':
            return return_list
        elif (not key or key == '1' or key == 1) and return_list != []:
            return return_list[0]

    def _add_stackable(self, entity):
        existing_entity = self.get(ID=entity.ID)
        if existing_entity:                             # entity exists in self
            existing_entity.quantity += 1
            entity.remove_old(entity)
        else:                                           # entity does not exist in self
            self.append(entity)

    def add(self, entity):
        if 'stackable' in entity.properties:
            self._add_stackable(entity)
        else:
            self.append(entity)

    def rem(self, entity):
        if 'stackable' in entity.properties and entity.quantity > 1:
            entity.quantity -= 1
        else:  # either (entity is stackable but entity.quantity = 1) or entity is not stackable
            self.remove(entity)

    def is_empty(self):
        return self == []