FROM --platform=linux/amd64 python:3.9-slim as build

WORKDIR /app
COPY app.py /app/
COPY manifests/pods.html /app/templates/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 80
CMD ["python", "app.py"]