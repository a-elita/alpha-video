FROM python:alpine
ARG ATOMICPARSLEY=0

RUN mkdir -p /usr/src/app
RUN if [ $ATOMICPARSLEY == 1 ]; then apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing atomicparsley; ln /usr/bin/atomicparsley /usr/bin/AtomicParsley; fi
COPY ./requirements.txt /usr/src/app/
RUN  pip install --no-cache-dir -r /usr/src/app/requirements.txt
COPY ./main.py /usr/src/app/

WORKDIR /usr/src/app

EXPOSE 5000

CMD [ "python", "-u", "./main.py" ]
