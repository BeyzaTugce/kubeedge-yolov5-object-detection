import base64
import json

import cv2
import numpy as np
import psutil
import torch
from flask import Flask, Response, request
from prometheus_client import Counter, Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Initialize the Flask application
app = Flask(__name__)

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Create a metric to track time spent, requests counts and resource usage.
REQUEST_TIME = Gauge('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('http_requests_total', 'Total post requests', ['method', 'endpoint'])
SYSTEM_USAGE = Gauge('system_usage', 'Current system resource usage', ['resource_type'])

@app.route("/detect", methods=["POST"])
@REQUEST_TIME.time()
def detect_objects():
    """
    Flas server listening image requests on port 5000 and running yolov5 object detection
    
    Returns: 
    --------  
    response: Flask Responsess
    """
    REQUEST_COUNT.labels('post', '/detect').inc()
    SYSTEM_USAGE.labels('cpu utilization').set(psutil.cpu_percent())
    SYSTEM_USAGE.labels('mem usage').set(psutil.virtual_memory().used)
    SYSTEM_USAGE.labels('available mem').set(psutil.virtual_memory().available)

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
 