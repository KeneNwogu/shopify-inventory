from flask import flash, redirect, url_for, render_template, request

from shopify.inventory.models import Inventory
from shopify.items.forms import ItemForm, DeleteItemForm
from shopify.items.models import Item

from flask import Blueprint

items = Blueprint('items', __name__)


@items.route('/item/<inventory_name>/add/', methods=['GET', 'POST'])
def add_inventory_item(inventory_name):
    form = ItemForm()
    if form.validate_on_submit():
        name = form.name.data
        quantity = form.quantity.data
        price = form.price.data
        sales = form.sales.data
        in_stock = form.in_stock.data

        item = Item(name=name, quantity=quantity, price=price, in_stock=in_stock, sales=sales)
        inventory = Inventory.get_inventory(inventory_name)
        inventory.add_item(item)

        flash(f'successfully created item for {inventory_name}')
        return redirect(url_for('inventory.inventory_items', inventory_name=inventory_name))
    inventory = Inventory.get_inventory(inventory_name)
    return render_template('item/add_item.html', form=form, inventory=inventory)


@items.route('/item/<inventory_name>/<item_id>/edit/', methods=['GET', 'POST'])
def edit_inventory_item(inventory_name, item_id):
    item = Item.get_item(item_id, inventory_name)
    form = ItemForm(name=item.name, quantity=item.quantity, price=item.price, in_stock=item.in_stock,
                    sales=item.sales)
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "quantity": form.quantity.data,
            "price": form.price.data,
            "sales": form.sales.data,
            "in_stock": form.in_stock.data
        }

        item.update(data=data, inventory_name=inventory_name)
        flash('successfully edited item')
        return redirect(url_for('inventory.inventory_items', inventory_name=inventory_name))
    return render_template('item/edit_item.html', form=form, inventory_name=inventory_name, item_id=item._id)


@items.route('/item/<inventory_name>/<item_id>/delete/', methods=['GET', 'POST'])
def delete_inventory_item(inventory_name, item_id):
    form = DeleteItemForm()
    item = Item.get_item(item_id, inventory_name)
    if form.validate_on_submit():
        inventory = Inventory.get_inventory(inventory_name)
        item.delete(inventory=inventory, comment=form.comment.data,
                    permanent_delete_time=form.permanent_delete_time.data)
        flash('successfully deleted item')
        return redirect(url_for('inventory.inventory_items', inventory_name=inventory_name))
    return render_template('item/delete_item.html', form=form, inventory_name=inventory_name, item_id=item._id,
                           item=item)


@items.route('/item/<inventory_name>/<item_id>/undo-delete/', methods=['GET'])
def undo_delete(inventory_name, item_id):
    item = Item.get_item(item_id, inventory_name)
    inventory = Inventory.get_inventory(inventory_name)
    inventory.undo_delete(item)
    return redirect(url_for('inventory.deleted_inventory_items', inventory_name=inventory_name))