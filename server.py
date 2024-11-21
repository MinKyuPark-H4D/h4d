from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for, send_from_directory
import json, os
app = Flask(__name__)

file_path = 'fake-soldier-data.json'
# Open and load the JSON data from the file
with open(file_path, 'r') as file:
    soldiers = json.load(file)['soldiers']
    
# ROUTES
@app.route('/')
def home_page():
   return render_template('home_page.html')   

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



