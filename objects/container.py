__author__ = 'Taylan Sengul'


class Container(list):
    # ========= OBJECTS HANDLING START =========
    # methods here asserts 'container' to be in self.properties
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

    def lookup(self, a_dict, key='1'):
        """
        usage: container.get({'ID': 'apple'}), container.get({'properties': 'red', 'properties': 'edible'})
        """
        # todo: shallow and deep search: an thing can be inside a container which is inside another container
        if a_dict == {} or set(a_dict.values()) == set(['']):
            return self
        return_list = []
        for entity in self:
            for search_attr in a_dict:
                entity_attr = getattr(entity, search_attr, None)
                if not (entity_attr and a_dict[search_attr] in entity_attr):
                    break
            else:
                return_list.append(entity)
        if key == 'all':
            return return_list
        elif (key == '1' or key == 1) and return_list != []:
            return return_list[0]

    def _add_stackable(self, entity):
        existing_entity = self.lookup({'ID': entity.ID})
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

    def remove(self, entity):
        if 'stackable' in entity.properties and entity.quantity > 1:
            entity.quantity -= 1
        else:  # either (entity is stackable but entity.quantity = 1) or entity is not stackable
            super(Container, self).remove(entity)

    def is_empty(self):
        return self == []