FROM jupyter/scipy-notebook

USER root
RUN apt-get update
RUN apt-get install build-essential software-properties-common -y

USER jovyan
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

COPY . /queue
WORKDIR /queue

RUN pip install -r requirements.txt

ENTRYPOINT celery -A tasks worker --loglevel=info
