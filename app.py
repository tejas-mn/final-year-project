import os
from flask import Flask, render_template, request
from flask import Flask,jsonify
from utils import *
import json

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join('static/', filename)
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

    return render_template('result.html' , data = context)

@app.route("/test")
def test():
    return render_template('test.html')


@app.route("/")
def index():
    return "Potato Leaf Disease Detection"

if __name__ == "__main__":
    app.run(debug=True)