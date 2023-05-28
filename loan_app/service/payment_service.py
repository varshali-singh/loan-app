from loan_app.enities import Loan, Status
from loan_app.storage.loan_info import get_loan_information_storage_instance
from loan_app.utils.authentication_utils import check_payment_info_parameters


def make_payment(payment_info):
    if not check_payment_info_parameters(payment_info):
        return "Pass correct parameters please."

    if payment_info["name"] == "admin":
        return "Login as a customer. You're currently logged in as an admin."

    loan = get_loan_information_storage_instance().get_loan_info(payment_info["name"])
    if not isinstance(loan, Loan) or loan.status == Status.PAID.name:
        return "No active loan found for the customer"

    next_payment = loan.payments[loan.installments_paid]
    amount_remaining = loan.total_amount - loan.amount_paid

    if payment_info["amount"] >= amount_remaining:
        next_payment.is_paid = True
        next_payment.amount_paid = payment_info["amount"]
        loan.status = Status.PAID.name
        loan.amount_paid = loan.total_amount
        loan.installments_paid += 1
        for i in range(loan.installments_paid, loan.tenure):
            loan.payments[i].is_paid = True
        return "Congratulations. You've succesfully paid your loan."
    elif payment_info["amount"] < next_payment.installment_amount:
        return "Please pay atleast the minimun amount due for an installment"
    elif payment_info["amount"] == next_payment.installment_amount:
        next_payment.is_paid = True
        next_payment.amount_paid = payment_info["amount"]
        loan.amount_paid += payment_info["amount"]
        loan.installments_paid += 1
        return "Payment made successfully"
    else:
        next_payment.is_paid = True
        next_payment.amount_paid = payment_info["amount"]
        loan.amount_paid += payment_info["amount"]
        loan.installments_paid += 1

        amount_remaining = loan.total_amount - loan.amount_paid
        new_amount_per_installment = amount_remaining / (
            loan.tenure - loan.installments_paid
        )
        for i in range(loan.installments_paid, loan.tenure):
            loan.payments[i].installment_amount = new_amount_per_installment
        return f"Payment made successfully. New amount per installment is {new_amount_per_installment}"
