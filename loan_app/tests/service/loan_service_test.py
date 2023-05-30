import unittest

from flask import Flask, Response
from loan_app.enities import Customer
from loan_app.service import loan_service
from loan_app.storage.customer_info_storage import (
    get_customer_information_storage_instance,
)


class LoanServiceTest(unittest.TestCase):
    def test_apply_for_loan_failure_for_incorrect_details(self):
        dummy_loan_details = {
            "customer_name": "loan_service_test_user",
            "password": "password",
        }
        output = loan_service.apply_for_loan(dummy_loan_details)

        self.assertEqual(output, "Please pass correct parameters for loan details.")

    def test_apply_for_loan_failure_for_admin_login(self):
        dummy_loan_details = {"customer_name": "admin", "amount": 100, "tenure": 10}
        output = loan_service.apply_for_loan(dummy_loan_details)

        self.assertEqual(
            output, "You're logged in as an admin. Please login as a customer."
        )

    def test_apply_for_loan_failure_for_user_not_found(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_loan_details = {
                "customer_name": "loan_service_test_user",
                "amount": 100,
                "tenure": 10,
            }

            output = loan_service.apply_for_loan(dummy_loan_details)

            self.assertEqual(output, "Please login as a registered user")

    def test_apply_for_loan_failure_for_user_already_has_loan(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_loan_details = {
                "customer_name": "loan_service_test_user_1",
                "amount": 100,
                "tenure": 10,
            }

            get_customer_information_storage_instance().store_customer_data(
                Customer("loan_service_test_user_1", "password", True)
            )

            output = loan_service.apply_for_loan(dummy_loan_details)

            self.assertEqual(
                output,
                "Customer already has a loan. Can't assign more than one loan to a customer",
            )

    def test_apply_for_loan_success(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_loan_details = {
                "customer_name": "loan_service_test_user_2",
                "amount": 100,
                "tenure": 10,
            }

            get_customer_information_storage_instance().store_customer_data(
                Customer("loan_service_test_user_2", "password", False)
            )

            output = loan_service.apply_for_loan(dummy_loan_details)

            self.assertEqual(
                output,
                "Applied for loan successfully, pending for admin approval",
            )

    def test_view_loan_details_failure_for_incorrect_details(self):
        dummy_customer_details = {"customer_name": "test_user", "password": "password"}
        output = loan_service.view_loan_details(dummy_customer_details)

        self.assertEqual(output, "Please provide correct user details")

    def test_view_loan_details_failure_unauthorized_access(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_user_details = {"name": "loan_service_test_user_2", "password": "p"}

            output = loan_service.view_loan_details(dummy_user_details)

            self.assertEqual(
                output,
                "Please provide correct user details",
            )

    def test_view_loan_details_success_for_admin(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_user_details = {"name": "admin", "password": "password"}

            output = loan_service.view_loan_details(dummy_user_details)

            self.assertIsInstance(output, Response)

    def test_view_loan_details_success_for_customer(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_user_details = {
                "name": "loan_service_test_user_2",
                "password": "password",
            }

            output = loan_service.view_loan_details(dummy_user_details)

            self.assertIsInstance(output, Response)

    def test_approve_loan_failure_for_incorrect_details(self):
        dummy_customer_loan_details = {"name": "test_user", "password": "password"}
        output = loan_service.approve_loan(dummy_customer_loan_details)

        self.assertEqual(
            output,
            "Either you're not logged in as Admin or provide correct customer_name of the loan",
        )

    def test_approve_loan_failure_unauthorized_access(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_user_details = {
                "name": "admin",
                "password": "p",
                "customer_name": "loan_service_test_user_2",
            }

            output = loan_service.approve_loan(dummy_user_details)

            self.assertEqual(
                output,
                "Either you're not logged in as Admin or provide correct customer_name of the loan",
            )

    def test_approve_loan_success(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_customer_details = {
                "name": "admin",
                "password": "password",
                "customer_name": "loan_service_test_user_2",
            }

            output = loan_service.approve_loan(dummy_customer_details)

            self.assertEqual(
                output,
                "Loan Approved",
            )

    def test_approve_loan_failure_for_no_active_loan_found(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_customer_details = {
                "name": "admin",
                "password": "password",
                "customer_name": "loan_service_test_user_new",
            }
            output = loan_service.approve_loan(dummy_customer_details)

            self.assertEqual(
                output,
                "No Loan Found for Customer",
            )


if __name__ == "__main__":
    unittest.main()
