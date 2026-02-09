from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from datetime import datetime
import re


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class ValidationError:
    code: str
    field: str
    message: str


class RowValidator:
    def __init__(self, rules: dict):
        self.rules = rules
        self.field_rules = rules.get("field_rules", {})

    def validate(self, row: dict) -> list[ValidationError]:
        errors: list[ValidationError] = []

        for field, rule in self.field_rules.items():
            value = row.get(field)

            if rule.get("required") and (value is None or value == ""):
                errors.append(ValidationError("REQUIRED_MISSING", field, f"{field} is required"))
                continue

            if value is None or value == "":
                continue

            if rule.get("type") == "decimal":
                try:
                    amount = Decimal(value)
                    if "min" in rule and amount < Decimal(str(rule["min"])):
                        errors.append(ValidationError("AMOUNT_BELOW_MIN", field, f"{field} below minimum"))
                except InvalidOperation:
                    errors.append(ValidationError("INVALID_DECIMAL", field, f"{field} invalid decimal"))

            if rule.get("type") == "numeric":
                if not str(value).isdigit():
                    errors.append(ValidationError("NOT_NUMERIC", field, f"{field} must be numeric"))
                if "length" in rule and len(str(value)) != int(rule["length"]):
                    errors.append(ValidationError("INVALID_LENGTH", field, f"{field} invalid length"))

            if rule.get("type") == "iso8601":
                try:
                    datetime.fromisoformat(str(value).replace("Z", "+00:00"))
                except Exception:
                    errors.append(ValidationError("INVALID_TIMESTAMP", field, f"{field} invalid timestamp"))

            if rule.get("type") == "email":
                if not EMAIL_REGEX.match(str(value)):
                    errors.append(ValidationError("INVALID_EMAIL", field, "invalid email format"))

            if "allowed_values" in rule:
                if value not in rule["allowed_values"]:
                    errors.append(ValidationError("INVALID_VALUE", field, f"{field} invalid value"))

        return errors
