class BankAccount:
    def __init__(self, init_balance: int) -> None:
        self._balance = init_balance
        
    @staticmethod
    def _validate_amount(amount: int) -> bool:
        if amount < 0:
            print("Amount should be positive or 0, got {}".format(amount))
        return amount >= 0

    def deposit(self, deposit_amount: int) -> None:
        if not self._validate_amount(deposit_amount):
            return

        self._balance += deposit_amount

    def withdraw(self, withdraw_amount: int) -> None:
        if not self._validate_amount(withdraw_amount):
            return
        
        if self._balance < withdraw_amount:
            print("Insufficient funds")
            return

        self._balance -= withdraw_amount

    @property
    def balance(self) -> int:
        return self._balance


if __name__ == "__main__":
    bank_account = BankAccount(10)
    print("Initial balance: ", bank_account.balance)

    bank_account.deposit(10)
    print("Deposit 10: ", bank_account.balance)

    bank_account.deposit(-10)
    print("Deposit -10: ", bank_account.balance)

    bank_account.withdraw(10)
    print("Withdraw 10: ", bank_account.balance)

    bank_account.withdraw(-10)
    print("Withdraw -10: ", bank_account.balance)

    bank_account.withdraw(100)
    print("Withdraw 100: ", bank_account.balance)
