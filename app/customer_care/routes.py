from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app.customer_care import customer_care
from .decorators import customer_care_required
from app.auth.models import User, Role
from app.admin.models import Order, PaymentDetail
from app import db
from flask_wtf.csrf import generate_csrf
from .forms import AssignTaskForm 

@customer_care.route("/")
@login_required
@customer_care_required
def dashboard():
    return render_template('customer_care/dashboard.html', title='User Dashboard')




@customer_care.route("/view_orders", methods=["GET", "POST"])
@login_required
@customer_care_required
def view_orders():
    # Fetch all orders
    orders = Order.query.all()

    # Fetch payment details for each order
    for order in orders:
        order.payment_details = PaymentDetail.query.filter_by(order_id=order.id).all()

    form = AssignTaskForm()  # Create an instance of the form

    if request.method == "POST":
        form.order_id.data = request.form.get("order_id")
        form.writer_id.data = request.form.get("writer_id")
        assigned_by = current_user.id  # Get the ID of the current user (customer care)

        # Assign the task to the writer
        order = Order.query.get(form.order_id.data)
        if order:
            order.assigned_to = form.writer_id.data  # Assign the order to the selected writer
            order.assigned_by = assigned_by  # Set the user who assigned the task
            order.status = "Assigned"  # Update the status
            db.session.commit()
            flash("Task assigned successfully!", "success")
        else:
            flash("Order not found!", "danger")

        return redirect(url_for("customer_care.view_orders"))

    # Fetch users with the role "writer"
    writer_role = Role.query.filter_by(name='writer').first()
    writers = writer_role.writer if writer_role else []

    csrf_token = generate_csrf()

    return render_template("customer_care/view_orders.html", orders=orders, writers=writers, csrf_token=csrf_token, form=form)


