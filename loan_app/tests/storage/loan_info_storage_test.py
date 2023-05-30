import unittest
from loan_app.enities import Customer, Loan, Status
from loan_app.storage.loan_info_storage import LoanInformationStorage


class LoanInfoStorageTest(unittest.TestCase):
    dummy_loan_data = Loan("id", "test", 10, 100, 0.0, [], 0, Status.PENDING.name)

    def test_store_loan_info_success(self):
        instance = LoanInformationStorage({})
        output = instance.store_loan_info(self.dummy_loan_data)

        self.assertEqual(output, None)
        self.assertEqual(len(instance.loan_data_dict), 1)

    def test_get_loan_info_success(self):
        instance = LoanInformationStorage({})
        instance.store_loan_info(self.dummy_loan_data)
        output = instance.get_loan_info(self.dummy_loan_data.customer_name)

        self.assertIsInstance(output, Loan)

    def test_get_loan_info_failure(self):
        customer_name = "user"

        output = LoanInformationStorage({}).get_loan_info(customer_name)

        self.assertNotIsInstance(output, Loan)
        self.assertEqual(output, "Customer doesn't have any loan")


if __name__ == "__main__":
    unittest.main()
