from decimal import Decimal

import bank


def test_account_creation_stores_salted_pin_hash(monkeypatch):
    bank.accounts.clear()
    answers = iter(["Arun", "1234567890", "1234"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    bank.create_account()

    account = bank.accounts["1234567890"]
    assert "pin" not in account
    assert account["pin_salt"]
    assert account["pin_hash"]
    assert bank.verify_pin("1234", account["pin_salt"], account["pin_hash"])
    assert not bank.verify_pin("9999", account["pin_salt"], account["pin_hash"])


def test_get_amount_handles_non_numeric_input(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "not-money")

    assert bank.get_amount("Amount: ") is None
    assert "valid amount" in capsys.readouterr().out


def test_get_amount_rejects_non_finite_and_non_positive_values(monkeypatch):
    for value in ("NaN", "Infinity", "0", "-2.50"):
        monkeypatch.setattr("builtins.input", lambda _prompt, value=value: value)
        assert bank.get_amount("Amount: ") is None


def test_debit_does_not_allow_overdraft(monkeypatch, capsys):
    account = {"balance": Decimal("50.00")}
    monkeypatch.setattr(bank, "get_amount", lambda _prompt: Decimal("60.00"))

    bank.debit(account)

    assert account["balance"] == Decimal("50.00")
    assert "Insufficient funds" in capsys.readouterr().out
