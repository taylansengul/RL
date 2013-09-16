class ResourceManager(object):
    resources_to_update = []

    @staticmethod
    def add_resource(resource):
        if resource not in ResourceManager.resources_to_update:
            ResourceManager.resources_to_update.append(resource)

    @staticmethod
    def remove_resource(resource):
        ResourceManager.resources_to_update.remove(resource)

    @staticmethod
    def manage():
        for j, resource in enumerate(ResourceManager.resources_to_update):
            resource.update()