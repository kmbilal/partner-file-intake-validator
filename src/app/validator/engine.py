import csv
import json
from pathlib import Path
from collections import Counter

from .rules_loader import RulesLoader
from .schema import RowValidator, ValidationError


class FileValidationEngine:
    def __init__(self, rules_path: str):
        self.rules = RulesLoader(rules_path).load()
        self.validator = RowValidator(self.rules)
        self.seen_transactions = set()
        self.error_counter = Counter()

    def process_file(self, input_file: str, output_dir: str):
        input_path = Path(input_file)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        valid_path = output_dir / "valid_records.csv"
        rejected_path = output_dir / "rejected_records.csv"
        report_path = output_dir / "validation_report.json"

        total = 0
        valid = 0
        invalid = 0

        with open(input_path, newline="", encoding="utf-8") as infile, \
             open(valid_path, "w", newline="", encoding="utf-8") as valid_file, \
             open(rejected_path, "w", newline="", encoding="utf-8") as rejected_file:

            reader = csv.DictReader(infile)

            required_columns = set(self.rules["required_columns"])
            if not required_columns.issubset(reader.fieldnames or []):
                raise ValueError("File missing required columns")

            valid_writer = csv.DictWriter(valid_file, fieldnames=reader.fieldnames)
            rejected_writer = csv.DictWriter(
                rejected_file,
                fieldnames=reader.fieldnames + ["error_codes", "error_reason"],
            )

            valid_writer.writeheader()
            rejected_writer.writeheader()

            for row in reader:
                total += 1

                errors: list[ValidationError] = self.validator.validate(row)

                tx = row.get("transaction_id")
                if tx in self.seen_transactions:
                    errors.append(ValidationError("DUPLICATE_TRANSACTION_ID", "transaction_id", "duplicate transaction_id"))
                else:
                    self.seen_transactions.add(tx)

                if errors:
                    invalid += 1
                    codes = [e.code for e in errors]
                    reason = "; ".join(e.message for e in errors)

                    self.error_counter.update(codes)

                    row_copy = dict(row)
                    row_copy["error_codes"] = ",".join(sorted(set(codes)))
                    row_copy["error_reason"] = reason
                    rejected_writer.writerow(row_copy)
                else:
                    valid += 1
                    valid_writer.writerow(row)

        risk_score = self._risk_score()
        risk_level = self._risk_level(invalid, total)

        top_issues = sorted(self.error_counter.items(), key=lambda x: x[1], reverse=True)[:3]
        top_issues = [{"code": c, "count": n} for c, n in top_issues]

        recommended_action = "ACCEPT"
        if risk_level in ("MEDIUM", "HIGH"):
            recommended_action = "REJECT"

        summary = (
            f"File processed: {total} records. "
            f"{valid} valid, {invalid} rejected. "
            f"Risk: {risk_level} (score={risk_score})."
        )

        report = {
            "total_records": total,
            "valid_records": valid,
            "invalid_records": invalid,
            "error_summary": dict(self.error_counter),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "top_issues": top_issues,
            "recommended_action": recommended_action,
            "summary": summary,
        }

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report

    def _risk_score(self) -> int:
        weights = {
            "DUPLICATE_TRANSACTION_ID": 7,
            "REQUIRED_MISSING": 5,
            "INVALID_TIMESTAMP": 4,
            "AMOUNT_BELOW_MIN": 4,
            "INVALID_DECIMAL": 4,
            "NOT_NUMERIC": 3,
            "INVALID_LENGTH": 2,
            "INVALID_EMAIL": 2,
            "INVALID_VALUE": 2,
        }

        score = 0
        for code, count in self.error_counter.items():
            score += weights.get(code, 1) * count
        return score

    def _risk_level(self, invalid: int, total: int) -> str:
        score = self._risk_score()
        if total == 0:
            return "UNKNOWN"
        if score >= 20:
            return "HIGH"
        if score >= 10:
            return "MEDIUM"
        return "LOW"
