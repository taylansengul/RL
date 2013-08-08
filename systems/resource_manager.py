class Resource_Manager(object):
    def __init__(self, game):
        self.game = game
        self.resources_to_update = []

    def add_resource(self, resource):
        self.resources_to_update.append(resource)

    def remove_resource(self, resource):
        self.resources_to_update.remove(resource)

    def manage(self):
        for resource in self.resources_to_update:
            resource.update()