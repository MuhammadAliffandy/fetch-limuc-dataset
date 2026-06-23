import os
import subprocess
import zipfile

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"ERROR executing: {cmd}")
    return result.returncode

def unzip_file(zip_path, extract_to):
    if not os.path.exists(zip_path):
        print(f"File {zip_path} not found. Skipping extraction.")
        return
    print(f"Extracting {os.path.basename(zip_path)} to {extract_to}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile:
        print(f"ERROR: {zip_path} is not a valid zip file or is corrupted.")

def main():
    base_dir = "/raid/D13K48009/texture/TMC"
    os.makedirs(base_dir, exist_ok=True)
    
    # Google Drive Folder ID for TMC-UCM from Colonoscopy-FetchDataset.ipynb
    folder_id = "1uonpqcs9ynI5lhlnSPmu0D6D6ApSs0xg"
    
    print(f"Downloading TMC dataset to {base_dir}...")
    
    # Note: gdown needs to be installed in the environment where this runs
    gdown_cmd = f"gdown --folder -O '{base_dir}' {folder_id}"
    run_cmd(gdown_cmd)
    
    augment_zip = os.path.join(base_dir, "augment.zip")
    images_zip = os.path.join(base_dir, "images.zip")
    
    print("Extracting downloaded zip files...")
    unzip_file(augment_zip, base_dir)
    unzip_file(images_zip, base_dir)
    
    # Cleanup
    for z in [augment_zip, images_zip]:
        if os.path.exists(z):
            print(f"Removing {z}...")
            os.remove(z)
            
    print("TMC Dataset fetched and extracted successfully!")

if __name__ == "__main__":
    main()
