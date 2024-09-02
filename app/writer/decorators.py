from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def writer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name not in ['writer', 'admin', 'customer_care']:
            flash("You don't have the permission to access the requested resource.", 'danger')
            return redirect(url_for(f"{current_user.role.name}.dashboard"))
        return f(*args, **kwargs)
    return decorated_function
