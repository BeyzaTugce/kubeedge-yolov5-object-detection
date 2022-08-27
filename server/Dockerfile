FROM python:3.9
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 5000
ENV PORT 5000
CMD exec gunicorn --bind :$PORT app:app --workers 1 --threads 1 