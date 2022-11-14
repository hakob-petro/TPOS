FROM python:3.10
COPY server.py /server/
COPY requirements.txt /server/
COPY config.json /server/
WORKDIR /server/
RUN pip3 install -r requirements.txt