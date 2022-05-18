from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    name = fields.StringField(validators=[DataRequired()])
    quantity = fields.IntegerField(validators=[DataRequired()])
    price = fields.IntegerField(validators=[DataRequired()])
    in_stock = fields.BooleanField(default=True)
    sales = fields.IntegerField(default=0)
    submit = fields.SubmitField('Add Item +')


class DeleteItemForm(FlaskForm):
    comment = fields.TextAreaField()
    permanent_delete_time = fields.DateTimeField(default=datetime.utcnow() + timedelta(days=7))
    submit = fields.SubmitField('Delete Item')