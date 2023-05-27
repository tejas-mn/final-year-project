from flask import Response, render_template, request,jsonify,Blueprint
from werkzeug.utils import secure_filename

from utils import *
from delete import *
import json
import os

main = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','JPG', 'JPEG', 'PNG'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/predict', methods=['POST'])
def predict(api=False):
    file = request.files['file']
    filename = file.filename

    if filename == '':
        return {"error" : "Please choose a file"}

    #If file exists and it is allowed
    if file and allowed_file(filename):
        
        file_path = os.path.join('static/', secure_filename(filename))
        
        file.save(file_path)
        print(file_path)

        image = cv2.imread(file_path)
        image = cv2.resize(image , (300,300))
        
        print(cv2.imwrite(file_path , image))

        context = prediction(file_path)

        js = {}
        with open('./assets/fungicides.json', 'r') as f:
            js = json.load(f)
        fungicides = []
        for fun in js['fungicides']:
            if fun['disease'] == context['disease']:
                fungicides.append(fun)
            if context['disease']=='Potato_healthy':
                fungicides.append(fun)

        context['fungicides'] = fungicides
        # return jsonify(context)
        
        q=""
        if(context['disease']=='Potato_Early_blight'):
            q="potato+early+blight&tbm=isch"
        elif(context['disease']=='Potato_Late_blight'):
            q="potato+late+blight&tbm=isch"
        else:
            q="potato+healthy+leaf&tbm=isch"

        ds = {}
        with open('./assets/disease.json', 'r') as f:
            ds = json.load(f)

        data = {}

        if(context['disease']=='Potato_Early_blight'):
            data["about_disease"] = ds['early']['about']
            data["symptoms"] = ds['early']['symptoms']['points']
            data['symptoms_para_1'] = ds['early']['symptoms']['desc_1']
            data['symptoms_para_2'] = ds['early']['symptoms']['desc_2']
            data['management_para_1'] = ds['early']['management']['desc']
            data['management'] = ds['early']['management']['points']

        elif(context['disease']=='Potato_Late_blight'):
            data["about_disease"] = ds['late']['about']
            data["symptoms"] = ds['late']['symptoms']['points']
            data['symptoms_para_1'] = ds['late']['symptoms']['desc_1']
            data['symptoms_para_2'] = ds['late']['symptoms']['desc_2']
            data['management_para_1'] = ds['late']['management']['desc']
            data['management'] = ds['late']['management']['points']        
        else:
            data["about_disease"] = ds['healthy']['about']
            data["symptoms"] = ds['healthy']['symptoms']['points']
            data['symptoms_para_1'] = ds['healthy']['symptoms']['desc_1']
            data['symptoms_para_2'] = ds['healthy']['symptoms']['desc_2']
            data['management_para_1'] = ds['healthy']['management']['desc']
            data['management'] = ds['healthy']['management']['points']

        # return 'http://127.0.0.1:5002/' + str(context['diseased_img'])[3:]

        if api:
            data['context'] = context
            return jsonify(data)
        
        return render_template('results.html' , data = context,query=q , info=data, title="Results")
    else:
        return Response("{'message':'Please choose an image'}", status=601, mimetype='application/json')

@main.route("/")
def index():
    return render_template('home.html', title="Home")


@main.route("/api/predict" , methods=['POST'])
def api():
    return predict(api=True)

@main.errorhandler(404) 
def invalid_route(e): 
    return jsonify({'errorCode' : 404, 'message' : 'Route not found'})