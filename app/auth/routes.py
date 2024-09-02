from flask import render_template, url_for, flash, redirect, request
from app import db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import Role, User
from flask_login import login_user, current_user, logout_user, login_required

from . import auth
@auth.route("/register/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        role_name = form.role.data  # Get role from the form
        role = Role.query.filter_by(name=role_name).first()  # Fetch the role from the DB
        user = User(username=form.username.data, email=form.email.data, phone_number=form.phone_number.data, password_hash=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role.name == 'employer':
            return redirect(url_for('employer.dashboard'))
        elif current_user.role.name == 'writer':
            return redirect(url_for('writer.dashboard'))
        elif current_user.role.name == 'customer_care':
            return redirect(url_for('customer_care.dashboard'))
        elif current_user.role.name == 'Admin':
            return redirect(url_for('admin.dashboard'))
        else:
            pass

    form = LoginForm()

    if form.validate_on_submit():
        # Find the user by username, email, or phone number
        user = User.query.filter(
            (User.username == form.username_email_phone.data) |
            (User.email == form.username_email_phone.data) |
            (User.phone_number == form.username_email_phone.data)
        ).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful', 'success')

            # Redirect to the appropriate dashboard based on role
            if user.role.name == 'employer':
                return redirect(url_for('employer.dashboard'))
            elif user.role.name == 'writer':
                return redirect(url_for('writer.dashboard'))
            elif user.role.name == 'customer_care':
                return redirect(url_for('customer_care.dashboard'))
            elif user.role.name == 'Admin':                   
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('public.dashboard'))
        else:
            flash('Login unsuccessful. Please check your credentials and try again.', 'danger')

    return render_template('auth/login.html', title='Login', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('public.dashboard'))
