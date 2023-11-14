# pull official base image
FROM python:3.11.4-slim-buster

EXPOSE 8000

# set work directory
WORKDIR /app 

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

#install and config supervisor
RUN pip install supervisor==4.2.5 
COPY ./supervisord.conf .
COPY ./celeryd.conf .
COPY ./celerybeat.conf .
RUN mkdir logs
RUN mkdir logs/supervisord
RUN mkdir logs/celery_logs

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/ .
RUN pip3 install -r develop.txt --no-cache-dir

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]


