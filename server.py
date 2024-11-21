from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for
import json
app = Flask(__name__)

file_path = 'fake-soldier-data.json'
# Open and load the JSON data from the file
with open(file_path, 'r') as file:
    soldiers = json.load(file)
    
# ROUTES
@app.route('/')
def home_page():
   return render_template('home_page.html')   

@app.route('/soldiers')
def view_soldiers():
    return render_template('soldiers.html', soldiers=soldiers)



if __name__ == '__main__':
   app.run(debug = True)



