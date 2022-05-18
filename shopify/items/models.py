from datetime import datetime

from bson import ObjectId

from shopify import mongo
from shopify.inventory.models import Inventory


class Item:
    def __init__(self, name, quantity, price, sales, in_stock, _id=ObjectId()):
        self._id = _id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.sales = sales
        self.in_stock = in_stock

    def create(self, inventory):
        date_created = datetime.utcnow()
        data = self.to_dict()
        data['date_created'] = date_created
        data['last_sale_date'] = None
        inventory.add_item(data)

    def update(self, data, inventory_name):
        data['_id'] = self._id
        mongo.db.inventories.update_one({'name': inventory_name, 'items._id': self._id}, {
            '$set': {
                'items.$': data
            }
        })

    def delete(self, inventory, comment, permanent_delete_time):
        inventory.delete_item(self, comment, permanent_delete_time)

    @staticmethod
    def get_item(item_id, inventory_name):
        inventory_items = Inventory.get_inventory(inventory_name, get_deleted=True).items
        items = list(filter(lambda x: x.get('_id') == ObjectId(item_id), inventory_items))
        if items:
            item = items[0]
            name = item.get('name')
            quantity = item.get('quantity')
            price = item.get('price')
            sales = item.get('sales')
            in_stock = item.get('in_stock')
            _id = item.get('_id')
            item_instance = Item(name=name, quantity=quantity, price=price, sales=sales, in_stock=in_stock, _id=_id)
            return item_instance

    def to_dict(self):
        return {
            '_id': self._id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'sales': self.sales,
            'in_stock': self.in_stock
        }