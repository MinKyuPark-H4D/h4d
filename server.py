from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for, send_from_directory, flash, send_file, after_this_request
import json, os, secrets, shutil
from datetime import datetime
from autofill import autofill_individual_soldier, autofill_uic
from doc_retreival import batch_doc_pull
from doc_validation import create_validation_report


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

file_path = 'fake-soldier-data.json'
# Open and load the JSON data from the file
with open(file_path, 'r') as file:
    soldiers = json.load(file)['soldiers']
    
# ROUTES
@app.route('/')
def home_page():
   return render_template('home_page.html')   

@app.route('/automation', methods=['GET', 'POST'])
def automation():
    uics = set(soldier['UIC'] for soldier in soldiers.values())

    if request.method == 'POST':
        
        # BATCH DOCUMENT PULLS
        if 'documentType' in request.form.keys():
            zip_file_path, folder_name = batch_doc_pull(request.form.get('unit'), request.form.get('documentType'), soldiers)
            @after_this_request
            def cleanup(response):
                try:
                    shutil.rmtree('temp_files')  # Remove the temp folder
                except Exception as e:
                    print(f"Error deleting temp files: {e}")
                return response
            return send_file(zip_file_path, as_attachment=True, download_name=f"{folder_name}.zip")
        # VALIDATION REPORT
        elif 'selectionType2' in request.form.keys():
            if request.form.get('selectionType2') == 'unit':
                uic = request.form.get('unitSelect2')
                csv_file_path = create_validation_report('unit', soldiers, uic=uic)
            else:
                soldier_id = request.form.get('soldierSelect2')
                csv_file_path = create_validation_report('individual', soldiers, soldier_id=soldier_id)
            @after_this_request
            def cleanup(response):
                # Delete the temporary file after the response is sent
                if os.path.exists(csv_file_path):
                    os.remove(csv_file_path)
                return response
            return send_file(csv_file_path, as_attachment=True, download_name=f"{csv_file_path}")    
                   
        else:
            # AUTOFILL
            selection_type = request.form.get('selectionType')  # 'unit' or 'soldier'
            if selection_type == 'unit':
                selected_unit = request.form.get('unitSelect')  # selected unit (UIC)
                print(f"Selected Unit: {selected_unit}")
                # Handle autofill for the entire unit
                autofill_uic(selected_unit)
                flash(f"Documents have been autofilled for the UIC: {selected_unit}", "success")
            elif selection_type == 'soldier':
                selected_soldier_id = request.form.get('soldierSelect')  # selected soldier ID
                print(f"Selected Soldier ID: {selected_soldier_id}")
                # run autofill script
                autofill_individual_soldier(selected_soldier_id)
                selected_soldier = soldiers[str(selected_soldier_id)]
                flash(f"Documents have been autofilled for {selected_soldier['rank']} {selected_soldier['first_name']} {selected_soldier['last_name']}.", "success")
        return redirect(url_for('automation')) 
    return render_template('automation.html', soldiers=soldiers, uics=uics)

@app.route('/soldiers')
def view_soldiers():
    return render_template('soldiers.html', soldiers=soldiers)

@app.route('/soldiers/<id>')
def view_soldier(id=None):
    soldier_folder = os.path.join('iPERMS', f'soldier_{id}')
    
    try:
        files = os.listdir(soldier_folder)
        files = [f for f in files if os.path.isfile(os.path.join(soldier_folder, f))]
    except FileNotFoundError:
        files = []

    # Get the modification date for each file
    file_data = []
    for file in files:
        file_path = os.path.join(soldier_folder, file)
        mod_time = os.path.getmtime(file_path)  # Get last modified time
        formatted_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')  # Format it into a human-readable string
        file_data.append({'name': file, 'modified': formatted_date})
    file_data.sort(key=lambda x: x['modified'], reverse=True)
    return render_template('view_soldier.html', soldier=soldiers[id], id=id, files=file_data)

@app.route('/documents/<path:filename>')
def download_file(filename):
    directory = os.path.join('iPERMS')
    return send_from_directory(directory, filename)

@app.route('/upload/<soldier_id>', methods=['POST'])
def upload_file(soldier_id):
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400

    # Get the filename and save it to the directory
    filename = file.filename
    directory = os.path.join(f'iPERMS/soldier_{soldier_id}')  # Directory where you want to save files
    
    # Check if the uploaded file exists and overwrite it
    file.save(os.path.join(directory, filename))  # This will overwrite the file if it exists
    return redirect(url_for('view_soldier', id=soldier_id))

if __name__ == '__main__':
   app.run(debug = True)



