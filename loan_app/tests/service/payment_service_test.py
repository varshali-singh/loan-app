import unittest

from flask import Flask
from loan_app.enities import Customer

from loan_app.service import loan_service, payment_service
from loan_app.storage.customer_info_storage import (
    get_customer_information_storage_instance,
)


class PaymentServiceTest(unittest.TestCase):
    def test_payment_service_failure_incorrect_parameters(self):
        dummy_parameters = {"name": "payment_service_test_user"}

        output = payment_service.pay_installment(dummy_parameters)

        self.assertEqual(output, "Pass correct parameters please.")

    def test_payment_service_failure_admin_login(self):
        dummy_parameters = {"name": "admin", "amount": 100}

        output = payment_service.pay_installment(dummy_parameters)

        self.assertEqual(
            output,
            "Please login as a customer. You're currently logged in as an admin.",
        )

    def test_payment_service_failure_no_active_loan(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_parameters = {"name": "payment_service_test_user", "amount": 100}

            get_customer_information_storage_instance().store_customer_data(
                Customer("payment_service_test_user", "password", True)
            )

            output = payment_service.pay_installment(dummy_parameters)

            self.assertEqual(output, "No active loan found for the customer")

    def test_payment_service_failure_paying_more_amount_than_required(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_parameters = {"name": "payment_service_test_user_1", "amount": 200}

            get_customer_information_storage_instance().store_customer_data(
                Customer("payment_service_test_user_1", "password", False)
            )
            loan_service.apply_for_loan(
                {
                    "customer_name": "payment_service_test_user_1",
                    "amount": 100,
                    "tenure": 10,
                }
            )
            loan_service.approve_loan(
                {
                    "name": "admin",
                    "password": "password",
                    "customer_name": "payment_service_test_user_1",
                }
            )
            output = payment_service.pay_installment(dummy_parameters)

            self.assertEqual(
                output, "Max payable amount is 100.0 whereas you are trying to pay 200"
            )

    def test_payment_service_failure_paying_less_amount_than_minimum_due(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_parameters = {"name": "payment_service_test_user_2", "amount": 5}

            get_customer_information_storage_instance().store_customer_data(
                Customer("payment_service_test_user_2", "password", False)
            )
            loan_service.apply_for_loan(
                {
                    "customer_name": "payment_service_test_user_2",
                    "amount": 100,
                    "tenure": 10,
                }
            )
            loan_service.approve_loan(
                {
                    "name": "admin",
                    "password": "password",
                    "customer_name": "payment_service_test_user_2",
                }
            )
            output = payment_service.pay_installment(dummy_parameters)

            self.assertEqual(
                output, "Please pay atleast the minimun amount due for an installment"
            )

    def test_payment_service_success_paying_remaining_loan_amount(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_parameters = {"name": "payment_service_test_user_3", "amount": 100}

            get_customer_information_storage_instance().store_customer_data(
                Customer("payment_service_test_user_3", "password", False)
            )
            loan_service.apply_for_loan(
                {
                    "customer_name": "payment_service_test_user_3",
                    "amount": 100,
                    "tenure": 10,
                }
            )
            loan_service.approve_loan(
                {
                    "name": "admin",
                    "password": "password",
                    "customer_name": "payment_service_test_user_3",
                }
            )
            output = payment_service.pay_installment(dummy_parameters)

            self.assertEqual(
                output, "Congratulations. You've succesfully paid your loan."
            )

    def test_payment_service_success_paying_more_amount_than_intallment_amount(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_parameters = {"name": "payment_service_test_user_4", "amount": 19}

            get_customer_information_storage_instance().store_customer_data(
                Customer("payment_service_test_user_4", "password", False)
            )
            loan_service.apply_for_loan(
                {
                    "customer_name": "payment_service_test_user_4",
                    "amount": 100,
                    "tenure": 10,
                }
            )
            loan_service.approve_loan(
                {
                    "name": "admin",
                    "password": "password",
                    "customer_name": "payment_service_test_user_4",
                }
            )
            output = payment_service.pay_installment(dummy_parameters)

            self.assertEqual(
                output, "Payment made successfully. New amount per installment is 9.0"
            )


if __name__ == "__main__":
    unittest.main()
