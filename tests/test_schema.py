from app.validator.rules_loader import RulesLoader


def test_rules_loader_reads_file():
    loader = RulesLoader("rules/settlement_v1.json")
    rules = loader.load()

    assert "required_columns" in rules
    assert "field_rules" in rules
    assert "transaction_id" in rules["field_rules"]
