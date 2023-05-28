from dataclasses import dataclass
from enum import Enum


@dataclass
class Customer:
    name: str
    password: str
    has_a_loan: bool


@dataclass
class Payment:
    loan_id: str
    installment_number: int
    installment_amount: float
    amount_paid: float
    is_paid: bool


@dataclass
class Loan:
    loan_id: str
    customer_name: str
    tenure: int
    total_amount: float
    amount_paid: float
    payments: list[Payment]
    installments_paid: int
    status: str


class Status(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    PAID = "paid"
