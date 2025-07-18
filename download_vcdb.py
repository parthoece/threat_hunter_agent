import os
import requests
from zipfile import ZipFile
from io import BytesIO

def download_and_extract_validated_vcdb(target_folder="data/vcdb"):
    repo_url = "https://github.com/vz-risk/VCDB/archive/refs/heads/master.zip"
    print(" Downloading VCDB repository ZIP...")
    
    response = requests.get(repo_url)
    if response.status_code != 200:
        raise Exception(f" Failed to download VCDB repo: {response.status_code}")

    print(" Extracting 'validated' and 'overridden' JSONs...")
    with ZipFile(BytesIO(response.content)) as zip_file:
        json_files = [
            f for f in zip_file.namelist()
            if (f.startswith("VCDB-master/data/json/validated/") or f.startswith("VCDB-master/data/json/overridden/"))
            and f.endswith(".json")
        ]

        os.makedirs(target_folder, exist_ok=True)

        for file in json_files:
            filename = os.path.basename(file)
            if filename:
                with open(os.path.join(target_folder, filename), "wb") as out_file:
                    out_file.write(zip_file.read(file))

    print(f" Extracted {len(json_files)} files to: {target_folder}")

if __name__ == "__main__":
    download_and_extract_validated_vcdb()
