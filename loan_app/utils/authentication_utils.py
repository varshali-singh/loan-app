from loan_app.enities import Customer
from loan_app.storage.customer_info_storage import (
    get_customer_information_storage_instance,
)


def authenticate_user(user_details) -> bool:
    user = get_customer_information_storage_instance().get_customer_data(
        user_details["name"]
    )
    if isinstance(user, Customer) and user.password == user_details["password"]:
        return True
    return False


def validate_loan_details(loan_details) -> bool:
    return (
        all(key in loan_details for key in ["customer_name", "tenure", "amount"])
        and int(loan_details["tenure"]) > 0
        and float(loan_details["amount"]) > 0
    )


def check_name_and_password_are_provided(data) -> bool:
    return all(key in data for key in ["name", "password"])


def check_payment_info_parameters(payment_info) -> bool:
    return all(key in payment_info for key in ["amount", "name"])
