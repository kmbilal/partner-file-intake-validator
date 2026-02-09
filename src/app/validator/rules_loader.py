import json
from pathlib import Path
from typing import Any, Dict


class RulesLoader:
    def __init__(self, rules_path: str):
        self.rules_path = Path(rules_path)
        self._rules: Dict[str, Any] | None = None

    def load(self) -> Dict[str, Any]:
        if not self.rules_path.exists():
            raise FileNotFoundError(f"Rules file not found: {self.rules_path}")

        with self.rules_path.open("r", encoding="utf-8") as f:
            self._rules = json.load(f)

        return self._rules

    @property
    def rules(self) -> Dict[str, Any]:
        if self._rules is None:
            return self.load()
        return self._rules

    def required_columns(self) -> list[str]:
        return list(self.rules.get("required_columns", []))

    def field_rules(self) -> Dict[str, Any]:
        return dict(self.rules.get("field_rules", {}))
