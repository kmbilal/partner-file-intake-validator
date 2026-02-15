# Partner File Intake Validator

Automated validation and triage system for vendor/partner data files.

This project simulates a real production workflow where external partners send CSV data files (transactions, settlements, reports, or records).  
Instead of manually reviewing files in Excel, the system automatically:

• validates the file  
• separates valid and invalid records  
• assigns structured error codes  
• produces a machine-readable report  
• calculates a risk level for the file

The goal is to act as a **data intake gate** before data enters internal systems.

---

## What problem this solves

Companies frequently receive data files from external sources:
- vendors
- payment processors
- affiliates
- accounting providers
- internal departments

These files often contain:
- missing fields
- duplicate records
- invalid timestamps
- malformed emails
- negative or incorrect amounts

Manual review wastes operational time and delays processing.

This system automates the review process.

---

## Outputs

After processing a file, the system produces:

**valid_records.csv**  
Records safe to import.

**rejected_records.csv**  
Records rejected with structured error codes and reasons.

**validation_report.json**  
Summary report including:
- error counts
- top issues
- risk score
- recommended action (ACCEPT / REJECT)

---

## Quick Demo (Recommended)

Clone the repo and run: ./scripts/demo_local.sh


This will:
1. Create a Python environment
2. Run validation
3. Generate outputs in `sample_data/output/`

---

## Serverless Demo (Lambda Simulation)

This project also runs as a local AWS Lambda using SAM + Docker.

This simulates a production environment where a file upload triggers automated processing.

---

## Example Use Cases

• Fintech settlement files  
• Marketplace vendor uploads  
• Affiliate commission reports  
• Accounting imports  
• Payroll or HR data ingestion  

---

## Future Extensions

- S3 automatic file trigger
- DynamoDB audit history
- Email/Slack notification on rejection
- API endpoint for upload

---

## Tech

Python, rules-based validation engine, structured error handling, local serverless simulation using AWS SAM and Docker.
