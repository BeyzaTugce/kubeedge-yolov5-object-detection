# YOLOv5 Object Detection Flask Server to be Deployed to Edge or Cloud servers

This project creates a Docker Image for running YOLOv5 object detection function as a Flask Server which listens on port 5000 "/detect" endpoint and a Prometheus Server which listens on port 5000 "/metrics" endpoint.
For testing in local, some images are exported from OpenCDA simulation and a client script is also created to send those images to the Flask server.

## Modules
There are two modules
  1. Client
  2. Server

### Client
The client reads images from the Images directory then converts each image to sendable format and stores as a JSON file in the format of JSON array [{"image": img_byte}, {}, ...]
The URL of Edge Node that the docker image of the server is deployed should be given in case of testing the deployment.

client -- |
          - client.py
          |     This code converts images to sendable format and stores in JSON then sends requests to the Flask server.
          |

### Server
The Flask server running yolov5 object detection listens image requests on port 5000 and routes to /detect endpoint. This project loads a pretrained YOLOv5 model from PyTorch Hub. 
All the image predictions are saved as pandas dataframe and converted to JSON object. Then, the HTTP response is sent to the client.
Prometheus server listens some metrics including request time, total request count, cpu utilization, memory usage and available memory routed to /metrics endpoint.  

```
server -- |
          - app.py
          |     This code runs the flask server
          |
          - requirements.txt
          |     This file is to install the dependencies
          |
          - Dockerfile
          |     This file is to build the Docker image
          |
```

## Setup and Run

### Deploy to edge nodes in KubeEdge cluster

#### Build a Docker image of the Flask application

```
docker build -t $PROJECT_NAME:$TAGNAME .
docker run -d -p 5000:5000 $PROJECT_NAME:$TAGNAME
docker push $DOCKER_HUB_ID/$PROJECT_NAME:$TAGNAME
```

### Deploy to Google Cloud Run as a remote cloud server

#### Setup GCP account
```
gcloud config set account $MY_EMAIL_ADDRESS
gcloud auth login $MY_EMAIL_ADDRESS
gcloud config set project $MY_PROJECT_ID
```
#### Build a Docker image of the Flask application

```
docker build -t gcr.io/$MY_PROJECT_ID/yolov5_detection_flask_app:v1 .
docker push gcr.io/$MY_PROJECT_ID/yolov5_detection_flask_app:v1
```

#### Select the Docker image from Container Registry and deploy on Cloud Run
```
gcloud run deploy yolov5_detection_flask_app-v1 \
 --image gcr.io/$MY_PROJECT_ID/yolov5_detection_flask_app:v1 \
 --region us-east1 \
 --platform managed \
 --memory 512Mi
```

