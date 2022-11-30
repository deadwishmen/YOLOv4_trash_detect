import cv2
import sys
import os
import glob
import re
from pathlib import Path

# Import fast.ai Library
from fastai import *
from fastai.vision import *

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]

class_name = []
with open('classes.txt', 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]
# print(class_name)
net = cv2.dnn.readNet('yolov4-custom_last.weights', 'yolov4-custom.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)



def model_predict(path, name):
    savePath = r'D:\YOLOv4_trash_predict\static\img'
    os.chdir(savePath)
    cap = cv2.imread(path)
    classes, scores, boxes = model.detect(cap, Conf_threshold, NMS_threshold)

    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]
        score[0] = round(score[0] * 100, 2)
        label = "%s : %s" % (class_name[classid[0]], score)
        cv2.rectangle(cap, box, color, 2)
        cv2.putText(cap, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 2)
    filename = name
    cv2.imwrite(filename, cap)
# def model_predict_yolov5(path, name):
    
    

# cv2.imshow("anh",cap)
# cv2.waitKey()
# cv2.destroyAllWindows()

@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        print(basepath)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        img_path = os.path.join(
            basepath, 'static\img', secure_filename(f.filename))
        f.save(file_path)
        print(file_path)
        name = f.filename
        # Make prediction
        model_predict(file_path, name)
        return name
    return None

if __name__ == '__main__':
    app.run(debug=True)
