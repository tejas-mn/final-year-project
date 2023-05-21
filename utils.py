import numpy as np
import cv2
import tensorflow as tf
import threading
from tensorflow.keras.preprocessing import image
# from lite import predictLite

# loading models
MODEL_PATH = './assets/Best_CNN_march_30_epoch.h5'
LITE_MODEL_PATH = './assets/cnn.tflite'
LABEL_PATH = './assets/labels.txt'

model = tf.keras.models.load_model(MODEL_PATH)
class_names = ['Potato_Early_blight', 'Potato_Late_blight', 'Potato_healthy']

Alpha = None
treshold = 170

def load_image(img_path):
    img = image.load_img(img_path, target_size=(256, 256))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    return img_tensor

def generate_mask(img_path):    
    img =  cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_green = cv2.inRange(hsv, (36, 0, 0), (86,255,255))
    mask_brown = cv2.inRange(hsv, (8, 60, 20), (30, 255, 255))
    mask_yellow = cv2.inRange(hsv, (14, 39, 64), (40, 255, 255))
    #mask = cv2.bitwise_or(mask_green, mask_brown)
    #mask = cv2.bitwise_or(mask, mask_yellow)
    mask = cv2.bitwise_not(mask_green)
    res = cv2.bitwise_not(img, img, mask= mask)
    new_file = img_path + "-new.jpg" 
    # print(new_file)
    cv2.imwrite(new_file , res)
    return new_file
    
def segment_image(file):
    img = cv2.imread(file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_green = np.array([25,0,20])
    upper_green = np.array([100,255,255])
    mask = cv2.inRange(hsv_img, lower_green, upper_green)
    result = cv2.bitwise_and(img, img, mask=mask)
    lower_brown = np.array([10,0,10])
    upper_brown = np.array([30,255,255])
    disease_mask = cv2.inRange(hsv_img, lower_brown, upper_brown)
    disease_result = cv2.bitwise_and(img, img, mask=disease_mask)
    final_mask = mask + disease_mask
    final_result = cv2.bitwise_and(img, img, mask=final_mask)
    # output_path='/Segmented/'+os.path.basename(os.path.dirname(file))+'/'+os.path.basename(file)
    new_file = file + "-segmented-.jpg" 
    cv2.imwrite(new_file,final_result)

    return new_file

def ProcessImage(img_path):
    OriginalImage = cv2.imread(img_path)
    b = OriginalImage[:, :, 0]
    g = OriginalImage[:, :, 1]
    r = OriginalImage[:, :, 2]
    Disease = r - g
    global Alpha
    Alpha = b
    GetAlpha(OriginalImage)
    ProcessingFactor = treshold
    for i in range(0, OriginalImage.shape[0]):
        for j in range(0, OriginalImage.shape[1]):
            if int(g[i, j]) > ProcessingFactor:
                Disease[i, j] = 255
    new_file = img_path + "-new-diseased.jpg" 
    perc_disease = DisplayDiseasePercentage(Disease)

    # print(new_file)
    cv2.imwrite(new_file , Disease)

    return (new_file,perc_disease)

def GetAlpha(OriginalImage):
    global Alpha
    for i in range(0, OriginalImage.shape[0]):
        for j in range(0, OriginalImage.shape[1]):
            if OriginalImage[i, j, 0] > 200 and OriginalImage[i, j, 1] > 200 and OriginalImage[i, j, 2] > 200:
                Alpha[i, j] = 255
            else:
                Alpha[i, j] = 0


def DisplayDiseasePercentage(Disease):
    Count = 0
    Res = 0
    for i in range(0, Disease.shape[0]):
        for j in range(0, Disease.shape[1]):
            if Alpha[i, j] == 0:
                Res += 1
            if Disease[i, j] < treshold:
                Count += 1
    Percent = (Count / Res) * 100
    return str(round(Percent, 2)) + "%"


def prediction(img_path):
    img_array = load_image(img_path)
    
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions[0])]
    
    confidence = round(100 * (np.max(predictions[0])), 2)
    print(predicted_class, confidence)

    #predicted_class,confidence,_ = predictLite(LITE_MODEL_PATH,img_path,LABEL_PATH)

    mask_img = generate_mask(img_path)
    # mask_img = segment_image(img_path)
    diseased_img , perc_disease = ProcessImage(img_path)

    context = {}
    if predicted_class == class_names[0]:
        context = {
            "disease" : predicted_class,
            "confidence" : confidence,
            "remedy": "Plant potato tubers with less water",
            "img_path" : "../" + img_path,
            "mask_img" : "../" + mask_img,
            "diseased_img" : "../" + diseased_img,
            "perc_disease" : perc_disease
        }
    elif predicted_class == class_names[1]:
        context = {
            "disease" : predicted_class,
            "confidence" : confidence,
            "remedy": "Plant potato tubers with more water",
            "img_path" : "../" + img_path,
            "mask_img" : "../" + mask_img,
            "diseased_img" : "../" + diseased_img,
            "perc_disease" : perc_disease
        }
    elif predicted_class == class_names[2]:
        context = {
            "disease" : predicted_class,
            "confidence" : confidence,
            "remedy": "NA",
            "img_path" : "../" +  img_path,
            "mask_img" : "../" + mask_img,
            "diseased_img" : "../" + diseased_img,
            "perc_disease" : perc_disease
        }
    return context