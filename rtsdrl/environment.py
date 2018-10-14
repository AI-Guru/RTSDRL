from .entities import Entity

class Environment:

    def __init__(self):
        self.entities = []
        self.entities_dict = {}

    def add_entity(self, entity):
        assert isinstance(entity, Entity), type(entity)
        self.entities.append(entity)
        self.entities_dict[entity.name] = entity
        entity.environment = self

    def get_percepts(self):
        return []

    def update(self, actions):

        # Let entities perform the actions.
        for entity_name, action in actions:
            entity = self.entities_dict[entity_name]
            entity.perform_action(action)
