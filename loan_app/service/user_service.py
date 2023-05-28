from flask import jsonify
from loan_app.enities import Customer, Loan
from loan_app.storage.customer_info import get_customer_information_storage_instance
from loan_app.storage.loan_info import get_loan_information_storage_instance
from loan_app.storage.payment_info import get_payment_information_storage_instance
from loan_app.utils.authentication_utils import (
    authenticate_user,
    check_name_and_password_are_provided,
)


def register_customer(customer_details):
    if (
        check_name_and_password_are_provided(customer_details)
        and customer_details["name"] != "admin"
    ):
        customer = Customer(
            name=customer_details["name"],
            password=customer_details["password"],
            has_a_loan=False,
        )
        return get_customer_information_storage_instance().store_customer_data(customer)
    else:
        return "Please provide name and password for registering the customer"


def login_customer(customer_details):
    if check_name_and_password_are_provided(customer_details) and authenticate_user(
        customer_details
    ):
        customer_info = get_customer_information_storage_instance().get_customer_data(
            customer_details["name"]
        )

        loan_info = get_loan_information_storage_instance().get_loan_info(
            customer_details["name"]
        )

        payment_info = "No corresponding payments found for loan"
        if isinstance(loan_info, Loan):
            payment_info = get_payment_information_storage_instance().get_payment_info(
                customer_details["name"]
            )

        output = {
            "customer_info": customer_info,
            "loan_info": loan_info,
            "payment_info": payment_info,
        }

        return jsonify(output)
    else:
        return "Please provide correct name and password for the customer"
