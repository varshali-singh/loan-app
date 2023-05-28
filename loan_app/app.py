from flask import Flask, request
from loan_app.enities import Customer

from loan_app.service import loan_service, user_service, payment_service
from loan_app.storage.customer_info import get_customer_information_storage_instance

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, world!"


@app.route("/register")
def register():
    return user_service.register_user(request.get_json())


@app.route("/login")
def login():
    return user_service.login_user(request.get_json())


@app.route("/apply_loan")
def apply_for_loan():
    return loan_service.apply_for_loan(request.get_json())


@app.route("/loan_details")
def view_loan_details():
    return loan_service.view_loan_details(request.get_json())


@app.route("/pay_installment")
def pay_loan_installment():
    return payment_service.make_payment(request.get_json())


@app.route("/approve_loan")
def approve_loan():
    return loan_service.approve_loan(request.get_json())


if __name__ == "__main__":
    customer = Customer(
        name="admin",
        password="password",
        has_a_loan=False,
    )
    get_customer_information_storage_instance().store_customer_data(customer)
    app.run(debug=True)
