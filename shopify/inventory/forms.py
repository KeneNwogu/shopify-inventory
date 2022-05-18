from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired


class InventoryForm(FlaskForm):
    name = fields.StringField(validators=[DataRequired()])
    submit = fields.SubmitField('Add Inventory +')