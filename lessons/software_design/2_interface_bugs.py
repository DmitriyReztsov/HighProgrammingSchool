class BankAccount:
    def __init__(self, init_balance: int) -> None:
        self._balance = init_balance
        
    def deposit(self, deposit_amount: int) -> None:
        self._balance += deposit_amount

    def withdraw(self, withdraw_amount: int) -> None:
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
    print("Withdraw 10: ", bank_account.balance)
