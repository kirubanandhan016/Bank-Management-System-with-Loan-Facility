from decimal import Decimal, InvalidOperation

accounts = {}


def get_amount(prompt):
    try:
        amount = Decimal(input(prompt))
    except InvalidOperation:
        print("Enter a valid amount.")
        return None

    if not amount.is_finite() or amount <= 0:
        print("Amount must be greater than zero.")
        return None

    return amount.quantize(Decimal("0.01"))


def create_account():
    print("\n========== CREATE ACCOUNT ==========")
    name = input("Enter your name: ").strip()
    if not name or not name.replace(" ", "").isalpha():
        print("Name must contain letters only.")
        return

    account_number = input("Enter a 10-digit account number: ").strip()
    if len(account_number) != 10 or not account_number.isdigit():
        print("Account number must contain exactly 10 digits.")
        return
    if account_number in accounts:
        print("Account number already exists.")
        return

    pin = input("Create a 4-digit PIN: ").strip()
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must contain exactly 4 digits.")
        return

    accounts[account_number] = {
        "name": name,
        "pin": pin,
        "balance": Decimal("0.00"),
        "loan_balance": Decimal("0.00"),
    }
    print(f"Account created for {name}. Account number: {account_number}")


def credit(account):
    amount = get_amount("Amount to credit: ")
    if amount is None:
        return
    account["balance"] += amount
    print(f"${amount:.2f} credited. Balance: ${account['balance']:.2f}")


def debit(account):
    amount = get_amount("Amount to debit: ")
    if amount is None:
        return
    if amount > account["balance"]:
        print("Insufficient funds.")
        return
    account["balance"] -= amount
    print(f"${amount:.2f} debited. Balance: ${account['balance']:.2f}")


def take_loan(account):
    amount = get_amount("Loan amount to request: ")
    if amount is None:
        return
    account["balance"] += amount
    account["loan_balance"] += amount
    print(f"Loan of ${amount:.2f} approved and added to your balance.")
    print(f"Outstanding loan: ${account['loan_balance']:.2f}")


def account_menu(account):
    while True:
        print("\n========== ACCOUNT MENU ==========")
        print("1. View balance and loan")
        print("2. Credit (deposit)")
        print("3. Debit (withdraw)")
        print("4. Take a loan")
        print("5. Log out")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print(f"Balance: ${account['balance']:.2f}")
            print(f"Outstanding loan: ${account['loan_balance']:.2f}")
        elif choice == "2":
            credit(account)
        elif choice == "3":
            debit(account)
        elif choice == "4":
            take_loan(account)
        elif choice == "5":
            print("Logged out.")
            return
        else:
            print("Invalid choice. Please try again.")


def login():
    account_number = input("Account number: ").strip()
    pin = input("PIN: ").strip()
    account = accounts.get(account_number)
    if account is None or account["pin"] != pin:
        print("Invalid account number or PIN.")
        return
    print(f"Welcome, {account['name']}.")
    account_menu(account)


def main_menu():
    print("\n====================================")
    print("              INDIAN BANK")
    print("====================================")
    while True:
        print("\n1. Create account")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Thank you for visiting KV Bank.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()