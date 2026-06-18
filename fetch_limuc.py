import os
import requests
import zipfile
from tqdm import tqdm
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_file(url, dest_path):
    response = requests.get(url, stream=True, verify=False)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024 # 1 Kibibyte
    
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=os.path.basename(dest_path))
    with open(dest_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print(f"ERROR: Something went wrong while downloading {os.path.basename(dest_path)}")

def unzip_file(zip_path, extract_to):
    print(f"Extracting {os.path.basename(zip_path)} to {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main():
    base_dir = "Dataset/LIMUC"
    os.makedirs(base_dir, exist_ok=True)
    
    files_to_download = [
        {
            "url": "https://zenodo.org/records/5827695/files/patient_based_classified_images.zip?download=1",
            "filename": "patient_based_classified_images.zip"
        },
        {
            "url": "https://zenodo.org/records/5827695/files/train_and_validation_sets.zip?download=1",
            "filename": "train_and_validation_sets.zip"
        },
        {
            "url": "https://zenodo.org/records/5827695/files/test_set.zip?download=1",
            "filename": "test_set.zip"
        }
    ]
    
    for file_info in files_to_download:
        url = file_info["url"]
        dest_path = os.path.join(base_dir, file_info["filename"])
        
        # Download
        if not os.path.exists(dest_path):
            print(f"Downloading {file_info['filename']}...")
            download_file(url, dest_path)
        else:
            print(f"{file_info['filename']} already exists. Skipping download.")
            
        # Extract
        unzip_file(dest_path, base_dir)
        
    print("LIMUC Dataset fetched and extracted successfully!")

if __name__ == "__main__":
    main()
