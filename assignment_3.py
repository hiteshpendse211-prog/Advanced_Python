from abc import ABC, abstractmethod
from datetime import datetime
import uuid
import functools

# ---------------- RECEIPT CLASS ----------------
class Receipt:
    def __init__(self, amount, method, status):
        self.txn_id = str(uuid.uuid4())[:8]
        self.amount = amount
        self.method = method
        self.status = status
        self.timestamp = datetime.now()

    def __str__(self):
        return (f"\n--- RECEIPT ---\n"
                f"Transaction ID : {self.txn_id}\n"
                f"Amount         : ₹{self.amount}\n"
                f"Method         : {self.method}\n"
                f"Status         : {self.status}\n"
                f"Time           : {self.timestamp}\n")


# ---------------- DECORATOR ----------------
def log_transaction(func):
    @functools.wraps(func)
    def wrapper(self, amount):
        print(f"\n[LOG] Starting transaction of ₹{amount} using {self.strategy.name}")
        result = func(self, amount)
        print(f"[LOG] Transaction Completed\n")
        return result
    return wrapper


# ---------------- STRATEGY BASE ----------------
class PaymentStrategy(ABC):
    name = "Generic Payment"

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass


# ---------------- CONCRETE STRATEGIES ----------------
class CreditCardPayment(PaymentStrategy):
    name = "Credit Card"

    def __init__(self, card_number, cvv, expiry):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def validate(self):
        return len(self.card_number) == 16 and len(self.cvv) == 3

    def pay(self, amount):
        if self.validate():
            return Receipt(amount, self.name, "SUCCESS")
        return Receipt(amount, self.name, "FAILED")


class PayPalPayment(PaymentStrategy):
    name = "PayPal"

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def validate(self):
        return "@" in self.email and len(self.password) >= 4

    def pay(self, amount):
        if self.validate():
            return Receipt(amount, self.name, "SUCCESS")
        return Receipt(amount, self.name, "FAILED")


class UPIPayment(PaymentStrategy):
    name = "UPI"

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def validate(self):
        return "@" in self.upi_id

    def pay(self, amount):
        if self.validate():
            return Receipt(amount, self.name, "SUCCESS")
        return Receipt(amount, self.name, "FAILED")


class NetBankingPayment(PaymentStrategy):
    name = "Net Banking"

    def __init__(self, bank_name, account_number):
        self.bank_name = bank_name
        self.account_number = account_number

    def validate(self):
        return len(self.account_number) >= 8

    def pay(self, amount):
        if self.validate():
            return Receipt(amount, self.name, "SUCCESS")
        return Receipt(amount, self.name, "FAILED")


# ---------------- CONTEXT CLASS ----------------
class PaymentProcessor:
    _registry = {}

    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        print(f"[CONFIG] Switching to {strategy.name}")
        self.strategy = strategy

    @log_transaction
    def process_payment(self, amount):
        if not self.strategy:
            raise Exception("No payment strategy set!")
        return self.strategy.pay(amount)

    @classmethod
    def register_strategy(cls, key, strategy_class):
        cls._registry[key] = strategy_class
        print(f"[REGISTRY] Registered {key}")

    @classmethod
    def available_methods(cls):
        return list(cls._registry.keys())

    @classmethod
    def create(cls, key, **kwargs):
        strategy_class = cls._registry.get(key)
        if not strategy_class:
            raise Exception("Invalid payment method!")
        return cls(strategy_class(**kwargs))


# ---------------- DRIVER CODE ----------------
if __name__ == "__main__":

    # Register strategies
    PaymentProcessor.register_strategy("upi", UPIPayment)
    PaymentProcessor.register_strategy("credit", CreditCardPayment)
    PaymentProcessor.register_strategy("paypal", PayPalPayment)
    PaymentProcessor.register_strategy("netbanking", NetBankingPayment)

    print("\nAvailable Payment Methods:", PaymentProcessor.available_methods())

    # Create processor with UPI
    processor = PaymentProcessor.create("upi", upi_id="user@bank")

    receipt = processor.process_payment(1500)
    print(receipt)

    # Switch to Credit Card
    processor.set_strategy(CreditCardPayment("1234567812345678", "123", "12/25"))
    print(processor.process_payment(2000))

    # Switch to Net Banking
    processor.set_strategy(NetBankingPayment("SBI", "12345678"))
    print(processor.process_payment(3000))

    # Invalid Payment Example
    processor.set_strategy(UPIPayment("invalidupi"))
    print(processor.process_payment(500)) 