FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install pip==9.0.3
RUN pip install wheel setuptools
RUN pip install -r requirements.txt
COPY . .
CMD [ "python3", "main.py"]
