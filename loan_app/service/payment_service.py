from loan_app.enities import Loan, Status
from loan_app.storage.customer_info_storage import (
    get_customer_information_storage_instance,
)
from loan_app.storage.loan_info_storage import get_loan_information_storage_instance
from loan_app.utils.authentication_utils import check_payment_info_parameters


def pay_installment(payment_info):
    if not check_payment_info_parameters(payment_info):
        return "Pass correct parameters please."

    if payment_info["name"] == "admin":
        return "Please login as a customer. You're currently logged in as an admin."

    loan = get_loan_information_storage_instance().get_loan_info(payment_info["name"])
    if not isinstance(loan, Loan) or loan.status == Status.PAID.name:
        return "No active loan found for the customer"

    next_payment = loan.payments[loan.installments_paid]
    amount_remaining = loan.total_amount - loan.amount_paid
    amount_paying = payment_info["amount"]
    if amount_paying > amount_remaining:
        return f"Max payable amount is {amount_remaining} whereas you are trying to pay {amount_paying}"
    elif amount_paying == amount_remaining:
        next_payment.is_paid = True
        next_payment.amount_paid = amount_paying
        loan.status = Status.PAID.name
        loan.amount_paid = loan.total_amount
        loan.installments_paid += 1
        for i in range(loan.installments_paid, loan.tenure):
            loan.payments[i].is_paid = True
            loan.payments[i].installment_amount = 0.0
        get_customer_information_storage_instance().get_customer_data(
            payment_info["name"]
        ).has_a_loan = False
        return "Congratulations. You've succesfully paid your loan."
    elif amount_paying < next_payment.installment_amount:
        return "Please pay atleast the minimun amount due for an installment"
    elif amount_paying == next_payment.installment_amount:
        next_payment.is_paid = True
        next_payment.amount_paid = amount_paying
        loan.amount_paid += amount_paying
        loan.installments_paid += 1
        return "Payment made successfully"
    else:
        next_payment.is_paid = True
        next_payment.amount_paid = amount_paying
        loan.amount_paid += amount_paying
        loan.installments_paid += 1

        amount_remaining = loan.total_amount - loan.amount_paid
        new_amount_per_installment = amount_remaining / (
            loan.tenure - loan.installments_paid
        )
        for i in range(loan.installments_paid, loan.tenure):
            loan.payments[i].installment_amount = new_amount_per_installment
        return f"Payment made successfully. New amount per installment is {new_amount_per_installment}"
