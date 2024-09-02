from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, IntegerField, MultipleFileField, FloatField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, NumberRange, Length
from app.admin.models import OrderType, PaperType, Format, Language

class PaymentDetailForm(FlaskForm):
    paper_type_id = SelectField('Paper Type', coerce=int, validators=[DataRequired()])
    pages = IntegerField('Pages', validators=[DataRequired(), NumberRange(min=1)])
    cost_per_page = FloatField('Cost per Page', validators=[DataRequired(), NumberRange(min=0.01)])
    total_cost = FloatField('Total Cost', render_kw={'readonly': True})

class OrderForm(FlaskForm):
    account_order_id = StringField('Account Order ID', validators=[DataRequired(), Length(max=50)])
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    order_type_id = SelectField('Order Type', coerce=int, validators=[DataRequired()])
    format_id = SelectField('Format', coerce=int, validators=[DataRequired()])
    language_id = SelectField('Language', coerce=int, validators=[DataRequired()])
    deadline_hours = IntegerField('Deadline (hours)', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('Description')
    files = MultipleFileField('Files')
    paper_details = FieldList(FormField(PaymentDetailForm), min_entries=1)


    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.order_type_id.choices = [(ot.id, ot.name) for ot in OrderType.query.all()]
        self.format_id.choices = [(f.id, f.name) for f in Format.query.all()]
        self.language_id.choices = [(l.id, l.name) for l in Language.query.all()]
        
        # Set choices for paper_type_id in all PaymentDetailForm instances
        paper_type_choices = [(pt.id, pt.name) for pt in PaperType.query.all()]
        for form in self.paper_details:
            form.paper_type_id.choices = paper_type_choices


