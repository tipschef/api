FROM python:3.8.8-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :8080 --workers 2 --worker-class uvicorn.workers.UvicornWorker  --threads 8 start_api:app
