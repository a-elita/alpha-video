FROM python:3.7.10-alpine3.13
RUN apk update && apk add libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev git nodejs npm nano wget curl net-tools unzip supervisor screen
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install pip==9.0.3
RUN pip install wheel setuptools
RUN pip install -r requirements.txt
RUN npm install -g localtunnel
COPY . .
EXPOSE 5000
ENV FLASK_ENV=development
ENV FLASK_APP=main.py
CMD [ "python3", "main.py"]
