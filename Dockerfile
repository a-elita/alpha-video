FROM python:3.6.6-alpine3.6
RUN apk update && apk add libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev git
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install pip==9.0.3
RUN pip install wheel setuptools
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/andrewstech/Flask-PyNgrok.git
COPY . .
EXPOSE 5000
ENV FLASK_ENV=development
ENV FLASK_APP=main.py
CMD [ "python3", "main.py"]
