from bson import ObjectId

from shopify import mongo


class Inventory:
    def __init__(self, name, items=[], _id=ObjectId()):
        self.name = name
        self.items = items
        self._id = _id

    def add_item(self, item):
        mongo.db.inventories.update_one({'_id': self._id}, {
            "$addToSet": {
                "items": item.to_dict()
            }
        })

    def create(self):
        inventory = mongo.db.inventories.insert_one({'name': self.name, 'items': self.items})
        self._id = inventory.inserted_id
        return self._id

    def edit(self):
        mongo.db.inventories.update_one({'_id': self._id}, {
            '$set': self.to_dict()
        })

    def to_dict(self):
        return {
            'name': self.name
        }

    def delete_item(self, item, comment, permanent_delete_time):
        mongo.db.inventories.update_one({'name': self.name, 'items._id': item._id}, {
            '$set': {
                'items.$.deleted': True,
                'items.$.comment': comment,
                'items.$.permanent_delete_time': permanent_delete_time
            }
        })

    def undo_delete(self, item):
        mongo.db.inventories.update_one({'name': self.name, 'items._id': item._id}, {
            '$unset': {
                'items.$.deleted': 1,
                'items.$.comment': 1,
                'items.$.permanent_delete_time': 1
            }
        })

    @staticmethod
    def inventories():
        return list(mongo.db.inventories.find())

    @staticmethod
    def get_inventory(name, get_deleted=False):
        inventory = mongo.db.inventories.find_one({'name': name})
        if not get_deleted:
            items = list(filter(lambda x: not x.get('deleted'), inventory.get('items')))
        else:
            items = inventory.get('items')
        inventory_instance = Inventory(name=inventory.get('name'), items=items,
                                       _id=inventory.get('_id'))
        return inventory_instance

    def get_deleted_items(self):
        inventory = mongo.db.inventories.find_one({'name': self.name})
        deleted_items = list(filter(lambda x: x.get('deleted'), inventory.get('items')))
        return deleted_items