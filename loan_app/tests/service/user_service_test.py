import unittest

from flask import Flask, Response
from loan_app.enities import Customer
from loan_app.service import user_service
from loan_app.storage.customer_info_storage import (
    get_customer_information_storage_instance,
)


class UserServiceTest(unittest.TestCase):
    def test_register_customer_success(self):
        dummy_customer_details = {"name": "test_user", "password": "password"}
        output = user_service.register_customer(dummy_customer_details)

        self.assertEqual(output, "Customer added successfully")

    def test_register_customer_failure_for_incorrect_user_details(self):
        dummy_customer_details = {"name": "test_user"}

        output = user_service.register_customer(dummy_customer_details)

        self.assertEqual(
            output, "Please provide name and password for registering the customer"
        )

    def test_register_customer_failure_for_admin_user_details(self):
        dummy_customer_details = {"name": "admin", "password": "password"}

        output = user_service.register_customer(dummy_customer_details)

        self.assertEqual(
            output,
            "You are trying to register as an admin which is not allowed. Please try some other username",
        )

    def test_login_customer_failure(self):
        dummy_customer_details = {"name": "user_test", "password": "password"}

        output = user_service.login_customer(dummy_customer_details)

        self.assertEqual(
            output, "Please provide correct name and password for the customer"
        )

    def test_login_customer_success(self):
        app = Flask(__name__)

        with app.app_context():
            dummy_customer_details = {
                "name": "user_service_test_user",
                "password": "password",
            }

            get_customer_information_storage_instance().store_customer_data(
                Customer("user_service_test_user", "password", False)
            )
            output = user_service.login_customer(dummy_customer_details)
            self.assertIsInstance(output, Response)


if __name__ == "__main__":
    unittest.main()
