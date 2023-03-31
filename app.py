from flask import Flask, render_template, request,jsonify
from werkzeug.utils import secure_filename
from utils import *
import json
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','JPG', 'JPEG', 'PNG'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    filename = file.filename

    if filename == '':
        return {"error" : "Please choose a file"}

    #If file exists and it is allowed
    if file and allowed_file(filename):
        
        file_path = os.path.join('static/', secure_filename(filename))
        file.save(file_path)

        context = prediction(file_path)
        js = {}
        with open('fungicides.json', 'r') as f:
            js = json.load(f)
        fungicides = []
        for fun in js['fungicides']:
            if fun['disease'] == context['disease']:
                fungicides.append(fun)

        context['fungicides'] = fungicides
        # return jsonify(context)
        return render_template('results.html' , data = context)
    else:
        return {"error" : "Invalid Image"}


@app.route("/")
def index():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)