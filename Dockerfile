FROM python:3.12-alpine3.19
WORKDIR /dagestan
COPY requirements.in start-web.sh src/ ./
RUN pip install --upgrade --no-cache-dir  pip-tools==7.4.1 && pip-compile /dagestan/requirements.in && pip install -r /dagestan/requirements.txt

