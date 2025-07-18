
import os
import json

def extract_ics_incidents(data_dir, fallback_if_empty=True):
    ics_incidents = []
    all_incidents = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            full_path = os.path.join(data_dir, filename)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_incidents.append(data)

                    asset_varieties = data.get("asset", {}).get("variety", [])
                    if any("ICS" in v or "Industrial Control" in v for v in asset_varieties):
                        ics_incidents.append(data)
            except Exception as e:
                print(f" Failed to parse {filename}: {e}")

    print(f" Total incident files loaded: {len(all_incidents)}")
    print(f" ICS-specific incidents found: {len(ics_incidents)}")

    if not ics_incidents and fallback_if_empty:
        print(" No ICS-related incidents found. Using all available incidents for demo/testing.")
        return all_incidents

    return ics_incidents
