from uuid import uuid4

from flask import jsonify
from loan_app.enities import Customer, Loan, Payment, Status
from loan_app.storage.customer_info import get_customer_information_storage_instance
from loan_app.storage.loan_info import get_loan_information_storage_instance
from loan_app.utils.authentication_utils import (
    authenticate_user,
    check_name_and_password_are_provided,
    validate_loan_details,
)


def apply_for_loan(loan_details):
    if validate_loan_details(loan_details):
        return "Please pass correct parameters for loan details."

    if loan_details["name"] == "admin":
        return "You're logged in as an admin. Please login as a customer."

    customer_data = get_customer_information_storage_instance().get_customer_data(
        loan_details["name"]
    )

    if isinstance(customer_data, Customer):
        if customer_data.has_a_loan == True:
            return "Customer already has a loan. Can't assign more than one loan to a customer"

        loan_id = str(uuid4())
        loan_amount = loan_details["amount"]
        loan_tenure = loan_details["tenure"]
        amount_per_payment = loan_amount / loan_tenure
        payments = []

        for week in range(1, loan_tenure + 1):
            payments.append(Payment(loan_id, week, amount_per_payment, 0.0, False))

        loan = Loan(
            loan_id,
            loan_details["name"],
            loan_tenure,
            loan_amount,
            0,
            payments,
            0,
            Status.PENDING.name,
        )

        get_loan_information_storage_instance().store_loan_info(loan)
        return "Applied for loan successfully"
    else:
        return "Please provide correct loan details or maybe you're logged in as admin. Please login as a registered user"


def view_loan_details(user_details):
    if check_name_and_password_are_provided(user_details) and authenticate_user(
        user_details
    ):
        if user_details["name"] == "admin":
            return jsonify(get_loan_information_storage_instance().loan_data_dict)
        else:
            return jsonify(
                get_loan_information_storage_instance().get_loan_info(
                    user_details["name"]
                )
            )
    else:
        return "Please provide correct user details"


def approve_loan(customer_loan_details):
    if (
        "admin_name" in customer_loan_details
        and "customer_name" in customer_loan_details
        and customer_loan_details["admin_name"] == "admin"
    ):
        loan = get_loan_information_storage_instance().get_loan_info(
            customer_loan_details["customer_name"]
        )

        if isinstance(loan, Loan):
            loan.status = Status.APPROVED.name
            get_customer_information_storage_instance().get_customer_data(
                customer_loan_details["customer_name"]
            ).has_a_loan = True
            return "Loan Approved"
        else:
            return "No Loan Found for Customer"
    else:
        return "Either you're not logged in as Admin or provide correct details of the loan"
