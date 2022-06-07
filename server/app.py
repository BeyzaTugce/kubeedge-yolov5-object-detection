import numpy as np
import json
import base64
import cv2
import torch

from flask import Flask, request, Response

# Initialize the Flask application
app = Flask(__name__)


@app.route("/detect", methods=["POST"])
def detect_objects():
    """
    Flas server listening image requests on port 5000 and running yolov5 object detection
    
    Returns: s
    --------  
    response: Flask Responsess
    """

    request_json = request.data.decode()
    images = json.loads(request_json)
    rgb_images = []

    for img in images:
        img['image']
        image = img["image"]
        image_dec = base64.b64decode(image)
        data_np = np.fromstring(image_dec, dtype='uint8')
        decoded_img = cv2.imdecode(data_np, 1)
        rgb_images.append(cv2.cvtColor(np.array(decoded_img), cv2.COLOR_BGR2GRAY))
		
    detection_model = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)
    results = detection_model(rgb_images)

    objects = []
    for i in range(len(results.pandas().xyxy)):
        obj = results.pandas().xyxy[i].to_json()
        objects.append(obj)

    #Send HTTP response
    res = json.dumps(objects)
    return Response(response=res, status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
 