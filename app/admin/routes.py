from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app.admin import admin
from app import db
from app.auth.models import User, Role
from .forms import RoleForm, UserForm, OrderTypeForm, PaperTypeForm, FormatForm, LanguageForm
from .decorators import admin_required
from .models import OrderType, PaperType, Format, Language

@admin.route("/")
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html', title='Admin Dashboard')

@admin.route('/manage_roles', methods=['GET', 'POST'])
@admin_required
def manage_roles():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data)
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully', 'success')
        return redirect(url_for('admin.manage_roles'))
    
    roles = Role.query.all()
    return render_template('admin/manage_roles.html', roles=roles, form=form)

@admin.route('/manage_users', methods=['GET', 'POST'])
@admin_required
def manage_users():
    form = UserForm()
    if form.validate_on_submit():
        role_id = form.role.data
        role = Role.query.get(role_id) if role_id != 0 else None
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.role = role
        db.session.add(user)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('admin.manage_users'))
    
    form.role.choices = [(0, 'Select a Role')] + [(role.id, role.name) for role in Role.query.all()]
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin/manage_users.html', users=users, roles=roles, form=form)

@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if request.method == 'GET':
        form.role.choices = [(0, 'Select a Role')] + [(role.id, role.name) for role in Role.query.all()]
        form.role.data = user.role_id if user.role else 0
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.set_password(form.password.data)
        user.role = Role.query.get(form.role.data) if form.role.data != 0 else None
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin.manage_users'))




@admin.route("/manage_entities", methods=['GET', 'POST'])
@login_required
@admin_required
def manage_entities():
    # Initialize forms
    order_type_form = OrderTypeForm()
    paper_type_form = PaperTypeForm()
    format_form = FormatForm()
    language_form = LanguageForm()

    form_type = request.form.get('form_type')

    if form_type == 'order_type' and order_type_form.validate_on_submit():
        new_order_type = OrderType(name=order_type_form.name.data)
        db.session.add(new_order_type)
        db.session.commit()
        flash('Order Type added successfully!', 'success')
        return redirect(url_for('admin.manage_entities'))

    elif form_type == 'paper_type' and paper_type_form.validate_on_submit():
        new_paper_type = PaperType(name=paper_type_form.name.data)
        db.session.add(new_paper_type)
        db.session.commit()
        flash('Paper Type added successfully!', 'success')
        return redirect(url_for('admin.manage_entities'))

    elif form_type == 'format' and format_form.validate_on_submit():
        new_format = Format(name=format_form.name.data)
        db.session.add(new_format)
        db.session.commit()
        flash('Format added successfully!', 'success')
        return redirect(url_for('admin.manage_entities'))

    elif form_type == 'language' and language_form.validate_on_submit():
        new_language = Language(name=language_form.name.data)
        db.session.add(new_language)
        db.session.commit()
        flash('Language added successfully!', 'success')
        return redirect(url_for('admin.manage_entities'))

    # Get existing entities for display
    order_types = OrderType.query.all()
    paper_types = PaperType.query.all()
    formats = Format.query.all()
    languages = Language.query.all()

    return render_template('admin/manage_entities.html', 
                           title='Manage Entities',
                           order_type_form=order_type_form,
                           paper_type_form=paper_type_form,
                           format_form=format_form,
                           language_form=language_form,
                           order_types=order_types,
                           paper_types=paper_types,
                           formats=formats,
                           languages=languages)
