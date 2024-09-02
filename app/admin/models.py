from datetime import datetime, timedelta
from app import db
from sqlalchemy import event


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_order_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    order_type_id = db.Column(db.Integer, db.ForeignKey('order_type.id'), nullable=False)
    format_id = db.Column(db.Integer, db.ForeignKey('format.id'), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=False)
    deadline_hours = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Pending Assignment')
    files = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    total_cost  = db.Column(db.Float, nullable=True)

    # Specify foreign keys for relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='orders', lazy=True)
    assigned_to_user = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_orders', lazy=True)
    assigned_by_user = db.relationship('User', foreign_keys=[assigned_by], backref='assigned_by_orders', lazy=True)

    # Relationship with PaymentDetail
    payment_details = db.relationship('PaymentDetail', backref='order', lazy=True)

    @property
    def deadline(self):
        return self.created_at + timedelta(hours=self.deadline_hours)

class OrderType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship with Order
    orders = db.relationship('Order', backref='order_type', lazy=True)


class PaperType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Paper type name (e.g., Word, PPT, Excel)

    # Relationship with PaymentDetail
    payment_details = db.relationship('PaymentDetail', backref='paper_type', lazy=True)


class PaymentDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    paper_type_id = db.Column(db.Integer, db.ForeignKey('paper_type.id'), nullable=False)  # ForeignKey to PaperType
    pages = db.Column(db.Integer, nullable=False)
    cost_per_page = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    @property
    def calculate_total_cost(self):
        return self.pages * self.cost_per_page

class Format(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationship with Order
    orders = db.relationship('Order', backref='format', lazy=True)

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationship with Order
    orders = db.relationship('Order', backref='language', lazy=True)
