from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for, send_from_directory, flash
import json, os, secrets
from autofill import autofill_individual_soldier, autofill_uic
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
    
    # List all files in the soldier's folder (filter out directories)
    try:
        files = os.listdir(soldier_folder)
        # Filter out non-files (just to be sure)
        files = [f for f in files if os.path.isfile(os.path.join(soldier_folder, f))]
    except FileNotFoundError:
        files = []

    return render_template('view_soldier.html', soldier=soldiers[id], id=id, files=files) 

@app.route('/documents/<path:filename>')
def download_file(filename):
    directory = os.path.join('iPERMS')
    return send_from_directory(directory, filename)

if __name__ == '__main__':
   app.run(debug = True)



