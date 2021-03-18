FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    

RUN mkdir -p /usr/src/app
COPY ./requirements.txt /usr/src/app/
RUN pip3 install -r /usr/src/app/requirements.txt
COPY ./main.py /usr/src/app/

WORKDIR /usr/src/app

EXPOSE 5000

CMD [ "python", "-u", "./main.py" ]
