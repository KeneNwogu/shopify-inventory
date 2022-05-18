from shopify import marsh
from marshmallow import fields
from datetime import datetime


class ItemSchema(marsh.Schema):
    _id = fields.Str()
    name = fields.Str()
    quantity = fields.Date()
    price = fields.Integer()
    sales = fields.Integer()
    in_stock = fields.Boolean(dump_default=True)
    date_created = fields.DateTime(dump_default=datetime.utcnow())
    last_sell_date = fields.DateTime(dump_default=None)


class InventorySchema(marsh.Schema):
    name = fields.Str()
    items = fields.List(fields.Nested(ItemSchema))
