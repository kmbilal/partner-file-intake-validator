from app.validator.rules_loader import RulesLoader
from app.validator.schema import RowValidator

def test_row_validation_detects_errors():
    rules = RulesLoader("rules/settlement_v1.json").load()
    validator = RowValidator(rules)

    bad_row = {
        "transaction_id": "TX1001",
        "merchant_id": "",
        "amount": "-20",
        "currency": "USD",
        "transaction_timestamp": "INVALIDDATE",
        "account_number": "123ABC",
        "email": "bademail",
    }

    errors = validator.validate(bad_row)
    codes = [e.code for e in errors]

    assert "REQUIRED_MISSING" in codes
    assert "INVALID_TIMESTAMP" in codes
    assert "INVALID_EMAIL" in codes
