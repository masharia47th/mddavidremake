from flask import Blueprint

customer_care = Blueprint('customer_care', __name__)

from app.customer_care import routes
