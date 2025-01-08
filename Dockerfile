FROM ubuntu:latest

RUN apt update && apt upgrade -y

RUN apt install -y -q build-essential python3-pip python3-dev
ENV PIP_BREAK_SYSTEM_PACKAGES 1

RUN pip3 install gunicorn uvloop httptools

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY service/ /app

ENV ACCESS_LOG=${ACCESS_LOG:-/proc/1/fd/1}
ENV ERROR_LOG=${ERROR_LOG:-/proc/1/fd/2}

ENTRYPOINT /usr/local/bin/gunicorn \
  -b 0.0.0.0:80 \
  -w 4 \
  -k uvicorn.workers.UvicornWorker main:app \
  --chdir /app \
  --access-logfile "$ACCESS_LOG" \
  --error-logfile "$ERROR_LOG"