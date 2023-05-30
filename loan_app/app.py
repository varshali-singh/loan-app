from flask import Flask, request
from loan_app.enities import Customer

from loan_app.service import loan_service, user_service, payment_service
from loan_app.storage.customer_info_storage import (
    get_customer_information_storage_instance,
)

app = Flask(__name__)


@app.route("/")
def index():
    customer = Customer(
        name="admin",
        password="password",
        has_a_loan=False,
    )
    get_customer_information_storage_instance().store_customer_data(customer)
    return "Welcome to Loan-App"


@app.route("/register_customer")
def register_customer():
    return user_service.register_customer(request.get_json())


@app.route("/login_customer")
def login_customer():
    return user_service.login_customer(request.get_json())


@app.route("/apply_loan")
def apply_for_loan():
    return loan_service.apply_for_loan(request.get_json())


@app.route("/loan_details")
def view_loan_details():
    return loan_service.view_loan_details(request.get_json())


@app.route("/pay_installment")
def pay_loan_installment():
    return payment_service.pay_installment(request.get_json())


@app.route("/approve_loan")
def approve_loan():
    return loan_service.approve_loan(request.get_json())


if __name__ == "__main__":
    app.run(debug=True)
