from flask import render_template, url_for, flash, redirect, request, current_app, send_file, abort 
from app import db
from app.employer.forms import OrderForm, PaymentDetailForm
from app.admin.models import Order, PaymentDetail
from flask_login import login_required, current_user
from .decorators import employer_required
from . import employer
from werkzeug.utils import secure_filename
import os


@employer.route("/dashboard/")
@login_required
@employer_required
def dashboard():
    return render_template("employer/dashboard.html", title="Employer Dashboard")


@employer.route("/add_task/", methods=["GET", "POST"])
@employer_required
def add_task():
    form = OrderForm()
    if form.validate_on_submit():
        # Create the order without the total cost
        new_order = Order(
            account_order_id=form.account_order_id.data,
            title=form.title.data,
            order_type_id=form.order_type_id.data,
            format_id=form.format_id.data,
            language_id=form.language_id.data,
            deadline_hours=form.deadline_hours.data,
            description=form.description.data,
            user_id=current_user.id,
        )

        db.session.add(new_order)
        db.session.flush()  # Flush to get the new_order.id before commit

        # Handle file uploads
        employer_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username)
        os.makedirs(employer_folder, exist_ok=True)
        uploaded_files = []
        for file in form.files.data:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(employer_folder, filename)
                file.save(file_path)
                uploaded_files.append(filename)

        if uploaded_files:
            new_order.files = ','.join(uploaded_files)

        # Save Payment Details and calculate total cost
        total_cost = 0
        for payment_detail in form.paper_details.data:
            calculated_total_cost = payment_detail['pages'] * payment_detail['cost_per_page']
            total_cost += calculated_total_cost
            new_payment_detail = PaymentDetail(
                order_id=new_order.id,
                paper_type_id=payment_detail['paper_type_id'],
                pages=payment_detail['pages'],
                cost_per_page=payment_detail['cost_per_page'],
                total_cost=calculated_total_cost
            )
            db.session.add(new_payment_detail)

        # Update the order with the calculated total cost
        new_order.total_cost = total_cost

        db.session.commit()

        flash('New task added successfully!', 'success')
        return redirect(url_for('employer.view_tasks'))

    return render_template("employer/add_task.html", form=form)


@employer.route("/view_tasks/", methods=["GET"])
@employer_required
def view_tasks():
    orders = Order.query.filter_by(user_id=current_user.id).all()

    for order in orders:
        order.payment_details = PaymentDetail.query.filter_by(order_id=order.id).all()

    return render_template("employer/view_tasks.html", orders=orders)


@employer.route('/download/<filename>')
@employer_required
def download_file(filename):
    # Define the directory where the files are stored, using an absolute path
    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username)

    # Join the filename with the user folder path
    file_path = os.path.join(user_folder, filename)

    if os.path.exists(file_path):
        print(f"File exists at {file_path}, preparing to send...")
        return send_file(file_path, as_attachment=True)
    else:
        print(f"File not found at {file_path}.")
        abort(404, description="File not found")
