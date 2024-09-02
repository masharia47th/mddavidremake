from flask import render_template, url_for
from flask_login import login_required

from .decorators import writer_required
from . import writer

@writer.route('/dashboard/')
@login_required
@writer_required
def dashboard():
    return render_template('writer/dashboard.html', title='Writer Dashboard')
