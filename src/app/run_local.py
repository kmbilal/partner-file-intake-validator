from app.validator.engine import FileValidationEngine

def main():
    engine = FileValidationEngine("rules/settlement_v1.json")
    report = engine.process_file(
        "sample_data/incoming/settlement_sample.csv",
        "sample_data/output",
    )
    print("Validation Complete")
    print(report)


if __name__ == "__main__":
    main()
