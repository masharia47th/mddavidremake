from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config_options
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

csrf = CSRFProtect()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    csrf.init_app(app)

    # Register Blueprints
    from app.auth import auth as auth_blueprint
    from app.admin import admin as admin_blueprint
    from app.public import public as public_blueprint
    from app.customer_care import customer_care as customer_care_blueprint
    from app.employer import employer as employer_blueprint  # Registering the employer blueprint
    from app.writer import writer as writer_blueprint  # Registering the writer blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(public_blueprint)
    app.register_blueprint(customer_care_blueprint, url_prefix='/customer_care')
    app.register_blueprint(employer_blueprint, url_prefix='/employer')  # Adding the employer blueprint
    app.register_blueprint(writer_blueprint, url_prefix='/writer')  # Adding the writer blueprint

    return app
