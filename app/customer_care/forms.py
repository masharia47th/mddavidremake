from flask_wtf import FlaskForm
from wtforms import SelectField, HiddenField
from wtforms.validators import DataRequired

class AssignTaskForm(FlaskForm):
    order_id = HiddenField('Order ID')
    writer_id = SelectField('Writer', validators=[DataRequired()])
