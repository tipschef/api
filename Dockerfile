FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY . /app
ARG PROJECT_ID
ARG PROJECT_ENV

RUN pip install -r /app/requirements.txt --no-cache-dir

WORKDIR /app

EXPOSE 80

ENV PYTHONPATH="/app"
ENV PROJECT_ID=${PROJECT_ID}
ENV PROJECT_ENV=${PROJECT_ENV}
