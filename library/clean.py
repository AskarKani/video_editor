import os, shutil
from pathlib import Path

def clean():
    for target in ["split_out", "merge_out"]:
        clean_path = Path(os.getcwd()) / target
        print("Cleaning the contents of " + str(clean_path))
        if os.path.isdir(clean_path):
            files = os.listdir(clean_path)
            for file in files:
                clean_file_dir = clean_path / file
                if os.path.isfile(clean_file_dir):
                    os.remove(clean_file_dir)
                elif os.path.isdir(clean_file_dir):
                    shutil.rmtree(clean_file_dir)
    print("Cleaning done......\n")