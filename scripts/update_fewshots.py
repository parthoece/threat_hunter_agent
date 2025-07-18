from src.extract_ics import extract_ics_incidents
from generate_fewshot import generate_fewshot_examples_from_vcdb, save_fewshots_to_yaml

def main():
    vcdb_path = "data/vcdb"
    print(f"Loading ICS data from: {vcdb_path}")
    
    ics_data = extract_ics_incidents(vcdb_path, fallback_if_empty=True)
    examples = generate_fewshot_examples_from_vcdb(ics_data)
    
    save_fewshots_to_yaml(examples, path="src/response_fewshots.yaml")

if __name__ == "__main__":
    main()
