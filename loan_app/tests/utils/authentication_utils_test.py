import unittest
from loan_app.enities import Customer

from loan_app.storage.customer_info_storage import (
    get_customer_information_storage_instance,
)
from loan_app.utils import authentication_utils


class AuthenticationUtilsTest(unittest.TestCase):
    def test_authentication_success(self):
        get_customer_information_storage_instance().store_customer_data(
            Customer(name="test_user", password="password", has_a_loan=False)
        )

        dummy_user_details = {"name": "test_user", "password": "password"}

        authentication_result = authentication_utils.authenticate_user(
            dummy_user_details
        )
        self.assertEqual(authentication_result, True)

    def test_authentication_failure_for_incorrect_password(self):
        get_customer_information_storage_instance().store_customer_data(
            Customer(name="test_user", password="password", has_a_loan=False)
        )

        dummy_user_details = {"name": "test_user", "password": "password_test"}

        authentication_result = authentication_utils.authenticate_user(
            dummy_user_details
        )
        self.assertEqual(authentication_result, False)

    def test_authentication_failure_for_no_user_found(self):
        dummy_user_details = {"name": "test_user", "password": "password_test"}

        authentication_result = authentication_utils.authenticate_user(
            dummy_user_details
        )
        self.assertEqual(authentication_result, False)

    def test_loan_details_validation_failure(self):
        dummy_loan_details = {"customer_name": "test_user", "tenure": 0, "amount": 0}

        authentication_result = authentication_utils.validate_loan_details(
            dummy_loan_details
        )
        self.assertEqual(authentication_result, False)

    def test_loan_details_validation_success(self):
        dummy_loan_details = {"customer_name": "test_user", "tenure": 100, "amount": 10}

        authentication_result = authentication_utils.validate_loan_details(
            dummy_loan_details
        )
        self.assertEqual(authentication_result, True)

    def test_name_password_validation_success(self):
        dummy_loan_details = {"name": "test_user", "password": "password"}

        authentication_result = (
            authentication_utils.check_name_and_password_are_provided(
                dummy_loan_details
            )
        )
        self.assertEqual(authentication_result, True)

    def test_name_password_validation_success(self):
        dummy_loan_details = {"name": "test_user"}

        authentication_result = (
            authentication_utils.check_name_and_password_are_provided(
                dummy_loan_details
            )
        )
        self.assertEqual(authentication_result, False)

    def test_payment_info_validation_success(self):
        dummy_loan_details = {"name": "test_user", "amount": 100}

        authentication_result = authentication_utils.check_payment_info_parameters(
            dummy_loan_details
        )
        self.assertEqual(authentication_result, True)

    def test_payment_info_validation_success(self):
        dummy_loan_details = {"name": "test_user"}

        authentication_result = authentication_utils.check_payment_info_parameters(
            dummy_loan_details
        )
        self.assertEqual(authentication_result, False)


if __name__ == "__main__":
    unittest.main()
