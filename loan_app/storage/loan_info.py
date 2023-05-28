from loan_app.enities import Loan

_instance_var = None


class LoanInformationStorage:
    def __init__(self, loan_data: dict) -> None:
        self.loan_data_dict = loan_data

    def get_loan_info(self, customer_name: str):
        if customer_name in self.loan_data_dict:
            return self.loan_data_dict[customer_name]
        else:
            return "Customer doesn't have any loan"

    def store_loan_info(self, loan_info: Loan) -> None:
        self.loan_data_dict[loan_info.customer_name] = loan_info


def get_loan_information_storage_instance() -> LoanInformationStorage:
    global _instance_var
    if _instance_var == None:
        _instance_var = LoanInformationStorage({})
    return _instance_var
