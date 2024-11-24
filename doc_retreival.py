import datetime, os, shutil
from zipfile import ZipFile 
def batch_doc_pull(uic, doc_type, soldiers, task_id=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if task_id:
        folder_name = f"{task_id}-{uic}-{doc_type}"
    else:
        folder_name = f"{timestamp}-{uic}-{doc_type}"

    # temp folder
    temp_folder = os.path.join("temp_files", folder_name)
    os.makedirs(temp_folder,exist_ok=True)

    soldier_ids = [soldier['id'] for soldier in soldiers.values() if soldier['UIC'] == uic]
    for soldier_id in soldier_ids:
        soldier_folder = os.path.join('iPERMS', f"soldier_{soldier_id}")
        if os.path.exists(soldier_folder):
            soldier_file = get_soldier_file(soldier_folder,doc_type)
            if soldier_file:
                first_name, last_name = soldiers[str(soldier_id)]['first_name'], soldiers[str(soldier_id)]['last_name']
                new_filename = f"{last_name}-{first_name}-{doc_type}"
                file_path = os.path.join(soldier_folder, soldier_file)
                # If the file exists, copy and rename it
                if os.path.exists(file_path):
                    new_file_path = os.path.join(temp_folder, new_filename)
                    shutil.copy(file_path, new_file_path)

    # return zip file for download
    zip_file_path = f"{temp_folder}.zip"
    with ZipFile(zip_file_path, 'w') as zipf:
        for file_name in os.listdir(temp_folder):
            zipf.write(os.path.join(temp_folder, file_name), arcname=file_name)

    return zip_file_path, folder_name


def get_soldier_file(soldier_folder, doc_type):
    soldier_file = None
    for file in os.listdir(soldier_folder):
        if file == doc_type:
            soldier_file = file

    return soldier_file