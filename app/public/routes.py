from flask import render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from . import public

@public.route("/")
def dashboard():
    return render_template('public/dashboard.html', title='Public Dashboard')
