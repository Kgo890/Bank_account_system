import json


def main():
    accounts = load_accounts()

    while True:
        print("--- Bank Account System ---")
        print("1. Create new account")
        print("2. View accounts")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            acc_num = int(input("Enter account number: "))
            balance = float(input("Enter your initial number: "))
            account = BankAccount(acc_num, balance)
            accounts.append(account)
            save_accounts(accounts)
            print(f"New Account {acc_num} created with a balance of {balance}")
        elif choice == '2':
            acc_num = int(input("Enter account number: "))
            found = False
            for acc in accounts:
                if acc.get_account_number() == acc_num:
                    print(f"Account {acc.get_account_number()}: Balance = ${acc.get_balance()}")
                    found = True
                    break
            if not found:
                print("Invalid account number")
        elif choice == '3':
            acc_num = int(input("Enter account number: "))
            amount = float(input("Enter the amount you want to deposit: "))
            for acc in accounts:
                if acc.get_account_number() == acc_num:
                    acc.deposit(amount)
                    save_accounts(accounts)
                    print(f"You just deposited {amount} into your {acc.get_account_number()} bank account")
                    print(f"The new balance is ${acc.get_balance()}")
                    break
                else:
                    print("Invalid account number")
        elif choice == '4':
            acc_num = int(input("Enter account number: "))
            amount = float(input("Enter the amount you want to withdraw: "))
            for acc in accounts:
                if acc.get_account_number() == acc_num:
                    try:
                        acc.withdraw(amount)
                        save_accounts(accounts)
                        print(f"You just withdrew {amount} into your {acc.get_account_number()} bank account")
                        print(f"The new balance is ${acc.get_balance()}")
                    except ValueError as e:
                        print(e)
                    break
                else:
                    print("Invalid account number")
        elif choice == '5':
            print("Exiting the program")
            break
        else:
            print('Invalid response, please pick a number between 1-5')


def save_accounts(accounts, filename='account-data.json'):
    data = [account.to_dict() for account in accounts]
    with open(filename, 'w') as f:
        json.dump(data, f)
        print("Accounts saved")


def load_accounts(filename='account-data.json'):
    try:
        with open(filename, 'r') as f:
            content = f.read()
            if not content.strip():
                return []
            data = json.loads(content)
        return [BankAccount.from_dict(acc) for acc in data]
    except FileNotFoundError:
        return []


class BankAccount:
    def __init__(self, account_number, initial_balance):
        self.__account_number = account_number
        self.__balance = initial_balance

    def get_account_number(self):
        return self.__account_number

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("cannot deposit zero or negative funds")
        else:
            self.__balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("cannot withdraw zero or negative funds")
        elif self.__balance < amount:
            raise ValueError("the amount you want to deposit is more than whats in your bank account")
        else:
            self.__balance -= amount

    def to_dict(self):
        return {
            'account_number': self.__account_number,
            'balance': self.__balance
        }

    def from_dict(data):
        return BankAccount(int(data['account_number']), float(data['balance']))


if __name__ == "__main__":
    main()
