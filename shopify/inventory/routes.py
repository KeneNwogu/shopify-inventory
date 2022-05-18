from flask import render_template, url_for, flash, redirect

from shopify.inventory.forms import InventoryForm
from shopify.inventory.models import Inventory

from flask import Blueprint

inventory = Blueprint('inventory', __name__)


@inventory.route('/')
@inventory.route('/inventories', methods=['GET'])
def all_inventories():
    inventories = Inventory.inventories()
    return render_template('inventory/inventories.html', inventories=inventories)


@inventory.route('/inventory/<inventory_name>', methods=['GET'])
def inventory_items(inventory_name):
    inventory_ = Inventory.get_inventory(inventory_name)
    return render_template('inventory/inventory.html', inventory=inventory_)


@inventory.route('/inventory/add/', methods=['GET', 'POST'])
def add_inventory():
    form = InventoryForm()
    if form.validate_on_submit():
        inventory_ = Inventory(name=form.name.data)
        inventory_.create()
        flash('successfully created inventory')
        return redirect(url_for('inventory.all_inventories'))
    return render_template('inventory/add_inventory.html', form=form)


@inventory.route('/inventory/<inventory_id>/edit/', methods=['GET', 'POST'])
def edit_inventory():
    form = InventoryForm()
    if form.validate_on_submit():
        inventory_ = Inventory(name=form.name.data)
        inventory_.edit()
        flash('successfully updated inventory')
        return redirect(url_for('inventory.inventory_items', inventory_name=inventory_.name))
    return render_template('inventory/edit_inventory.html', form=form)


@inventory.route('/inventory/<inventory_name>/deleted/', methods=['GET'])
def deleted_inventory_items(inventory_name):
    inventory_ = Inventory.get_inventory(inventory_name)

    return render_template('inventory/deleted_inventory_items.html', deleted_items=inventory_.get_deleted_items(),
                           inventory=inventory_)




