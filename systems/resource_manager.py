class Resource_Manager(object):
    def __init__(self, game):
        self.game = game
        self.resources_to_update = []

    def add_to_update_list(self, resource):
        self.resources_to_update.append(resource)

    def manage(self):
        for resource in self.resources_to_update:
            resource.update()