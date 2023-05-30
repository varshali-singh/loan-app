from loan_app.enities import Customer

_instance_var = None


class CustomerInformationStorage:
    def __init__(self, customer_data: dict) -> None:
        self.customer_data_dict = customer_data
        self.store_customer_data(Customer("admin", "password", False))

    def get_customer_data(self, customer_name: str):
        if customer_name in self.customer_data_dict:
            return self.customer_data_dict[customer_name]
        else:
            return "Customer doesn't exist"

    def store_customer_data(self, customer_data: Customer) -> str:
        if customer_data.name in self.customer_data_dict:
            return "Customer already exists"
        else:
            self.customer_data_dict[customer_data.name] = customer_data
            return "Customer added successfully"


def get_customer_information_storage_instance() -> CustomerInformationStorage:
    global _instance_var
    if _instance_var == None:
        _instance_var = CustomerInformationStorage({})
    return _instance_var
