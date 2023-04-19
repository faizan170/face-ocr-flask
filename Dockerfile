FROM python:3.9-slim

RUN apt-get update && apt-get install -y tesseract-ocr ffmpeg libsm6 libxext6


COPY requirements.txt ./

# Install production dependencies.
#ADD requirements.txt .
RUN pip install -r requirements.txt

# Copy local code to the container image.
WORKDIR /app
COPY . .

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --log-level debug --timeout 0 main:app