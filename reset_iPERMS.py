#!/usr/bin/env python3
import os, glob, shutil
base_folder='iPERMS'
# Traverse all directories inside the base folder (assuming the folders are named like "soldier_{id}")
for soldier_folder in os.listdir(base_folder):
    soldier_folder_path = os.path.join(base_folder, soldier_folder)
    
    # Check if it's a directory (soldier folder)
    if os.path.isdir(soldier_folder_path):
        # Search for all PDF files within the current soldier's directory
        pdf_files = glob.glob(os.path.join(soldier_folder_path, "*.pdf"))
        
        for pdf_file in pdf_files:
            # Only delete files that don't end with 'HS_Diploma.pdf'
            if not pdf_file.endswith("HS_Diploma.pdf"):
                try:
                    os.remove(pdf_file)
                    print(f"Deleted file: {pdf_file}")
                except Exception as e:
                    print(f"Error deleting {pdf_file}: {e}")
# remove temp_files
shutil.rmtree('temp_files')