from uuid import uuid4


class Variable:

    def __init__(self):
        self.__class__ == 'Variable'
        self.subscribers = {}
        self.uuid = uuid4()

    def on_data(self, snapshot):
        for subscriber in self.subscribers:
            subscriber.on_new_value(snapshot, self.uuid)

    def get_uuid(self):
        return self.uuid

    def add_subscriber(self, relationship):
        self.subscribers[relationship.get_uuid()] = relationship

    def remove_subscriber(self, relationship_uuid):
        self.subscribers.pop(relationship_uuid, None)

