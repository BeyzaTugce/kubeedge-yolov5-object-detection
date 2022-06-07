import numpy as np
import json
import base64
import cv2
import requests
import glob

# Write the URL of Google Cloud Run that the docker image of the server is deployed
CLOUD_RUN_URL = ""

def send_image():
    """
    Sending images saved from OpenCDA simulation to the Flask server deployed to the Google Cloud Run listening image requests on port 5000 and running yolov5 object detection
    
    Returns: 
    --------  
    objects: Array of json dictionaries for detected objects 
    """
    images = []
    
    for img in glob.glob("images/*.jpg"):
        #Convert image to sendable format and store in JSON
        image = cv2.imread(img)
        _, encimg = cv2.imencode(".jpg ", image)
        img_str = encimg.tostring()
        img_byte = base64.b64encode(img_str).decode("utf-8")
        images.append({'image': img_byte})

    img_json = json.dumps(images)

    #Send HTTP request
    response = requests.post(f"{CLOUD_RUN_URL}/detect", data=img_json)

    objects = json.loads(response.text)
    for img_obj in objects:
        img_dict = json.loads(img_obj)
        print(img_dict)
    
    return objects

if __name__ == '__main__':
    send_image()