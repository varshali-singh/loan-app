from loan_app.enities import Payment

_instance_var = None


class PaymentInformationStorage:
    def __init__(self, payment_data: dict) -> None:
        self.payment_data_dict = payment_data

    def get_payment_info(self, loan_id: str):
        if loan_id in self.payment_data_dict:
            return self.payment_data_dict[loan_id]
        else:
            return "No corresponding payment for loan"


def get_payment_information_storage_instance() -> PaymentInformationStorage:
    global _instance_var
    if _instance_var == None:
        _instance_var = PaymentInformationStorage({})
    return _instance_var
