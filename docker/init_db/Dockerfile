FROM python:3.10
COPY init.py /init_db/
COPY requirements.txt /init_db/
COPY config.json /init_db/
WORKDIR /init_db/
RUN mkdir /init_db/data && pip3 install -r requirements.txt