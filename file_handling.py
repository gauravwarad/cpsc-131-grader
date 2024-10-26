import os
import zipfile
import subprocess
import shutil
import re

from grader import grade_driver

# Method to extract a zip file
def extract_zip(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile:
        print(f"Error: {zip_path} is not a valid zip file.")

# Method to handle the recursive extraction and execution of zip files
def process_zip(zip_path, extraction_dir, student_name):
    extract_zip(zip_path, extraction_dir)
    # Traverse the extracted contents
    for root, dirs, files in os.walk(extraction_dir):
        for file in files:
            # If the extracted file is a zip, process it further
            file_path = os.path.join(root, file)
            if file.endswith('.zip'):
                process_zip(os.path.join(root, file), 
                            os.path.join(root, file.replace('.zip', '')),
                            student_name)
            elif file.endswith('.cpp'):
                if validate_files(file_path):
                    grade_driver(file_path, student_name)

# Main method to iterate through all files in the submissions folder
def process_submissions(submissions_folder):
    for root, dirs, files in os.walk(submissions_folder):
        for file in files:
            student_name = file.split("_")[0]
            print("student name is - ", student_name)
            file_path = os.path.join(root, file)
            # If the file is a .cpp file, validate_files it
            if file.endswith('.cpp'):
                if validate_files(file_path):
                    grade_driver(file_path, student_name)

            # If the file is a .zip file, process it
            elif file.endswith('.zip'):
                extract_dir = os.path.join(root, file.replace('.zip', ''))
                process_zip(file_path, extract_dir, student_name)


# Method to validate_files a .cpp file
def validate_files(filepath):

    try:
        if filepath.endswith("GroceryItem.cpp"):
            print("File matches the required pattern. - ", filepath)
            return True
        else:
            print("File does not match the required pattern. - ", filepath)
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error validating (validate_files) {filepath}: {e}")
        return False