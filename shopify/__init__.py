import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI') or 'mongodb://127.0.0.1:27017/shopify'

mongo = PyMongo()
marsh = Marshmallow()

mongo.init_app(app)
marsh.init_app(app)

from shopify.inventory.routes import inventory
from shopify.items.routes import items

app.register_blueprint(inventory)
app.register_blueprint(items)