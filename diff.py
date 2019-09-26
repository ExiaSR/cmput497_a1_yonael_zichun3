"""
Check if our attempt to cleanup duplicate is working
"""

import subprocess
import os

def get_output_files(dir="output"):
    (dirpath, _, filenames) = next(os.walk(dir))
    return {
        filename: os.path.join(dirpath, filename)
        for filename in filenames
        if filename.endswith(".tsv")
    }

def main():
    original = get_output_files()
    clean = get_output_files(dir="output_old")

    for filename, path in original.items():
        print("Running diff againt {} and {}".format(path, clean[filename]))
        subprocess.run(["diff", path, clean[filename]])

if __name__ == "__main__":
    main()
