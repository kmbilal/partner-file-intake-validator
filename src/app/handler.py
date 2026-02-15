import json
import os
from app.validator.engine import FileValidationEngine


def handler(event, context):
    """
    Local SAM/Lambda handler.

    Event format:
      {
        "rules_path": "rules/settlement_v1.json",
        "input_file": "sample_data/incoming/settlement_sample.csv",
        "output_dir": "/tmp/output"   # optional
      }
    """
    rules_path = event.get("rules_path", "rules/settlement_v1.json")
    input_file = event.get("input_file", "sample_data/incoming/settlement_sample.csv")

    # Lambda/SAM: write only to /tmp (writable). Default there.
    output_dir = event.get("output_dir") or "/tmp/output"

    engine = FileValidationEngine(rules_path)
    report = engine.process_file(input_file, output_dir)

    # Helpful: return where files were written in Lambda
    report["_output_dir"] = output_dir

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(report),
    }
