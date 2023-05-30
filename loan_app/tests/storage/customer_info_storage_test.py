import unittest
from loan_app.enities import Customer
from loan_app.storage.customer_info_storage import CustomerInformationStorage


class CustomerInfoStorageTest(unittest.TestCase):
    def test_store_customer_data_success(self):
        dummy_customer_data = Customer(
            name="test_user", password="password", has_a_loan=False
        )
        instance = CustomerInformationStorage({})
        output = instance.store_customer_data(dummy_customer_data)

        self.assertEqual(output, "Customer added successfully")
        self.assertEqual(len(instance.customer_data_dict), 2)

    def test_store_customer_data_failure(self):
        dummy_customer_data = Customer(
            name="test_user", password="password", has_a_loan=False
        )
        instance = CustomerInformationStorage({})
        output1 = instance.store_customer_data(dummy_customer_data)
        output2 = instance.store_customer_data(dummy_customer_data)

        self.assertIsInstance(output1, str)
        self.assertEqual(output2, "Customer already exists")
        self.assertEqual(len(instance.customer_data_dict), 2)

    def test_get_customer_data_success(self):
        dummy_customer_data = Customer(
            name="test_user", password="password", has_a_loan=False
        )

        instance = CustomerInformationStorage({})
        instance.store_customer_data(dummy_customer_data)
        output = instance.get_customer_data(dummy_customer_data.name)

        self.assertIsInstance(output, Customer)

    def test_get_customer_data_failure(self):
        customer_name = "user"

        output = CustomerInformationStorage({}).get_customer_data(customer_name)

        self.assertNotIsInstance(output, Customer)
        self.assertEqual(output, "Customer doesn't exist")


if __name__ == "__main__":
    unittest.main()
