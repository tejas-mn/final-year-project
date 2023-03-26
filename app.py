import os
import numpy as np
import cv2
import pandas as pd
from PIL import Image
import tensorflow as tf
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, request
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
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

    return render_template('result.html' , data = context, rec=fungicides)

@app.route("/test")
def test():
    return render_template('test.html')


@app.route("/")
def index():
    return "Potato Leaf Disease Detection"

if __name__ == "__main__":
    app.run(debug=True)