FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	python3-psycopg2 \
	git

WORKDIR /

COPY requirements.txt /

RUN pip3 install --upgrade pip && \
	pip3 install -r requirements.txt

WORKDIR /app

# Download the rpc files.
RUN git clone https://github.com/googleapis/googleapis.git

# Copy the source code.
COPY . ./

# # Copy the frontend build
# RUN mkdir ./static && \
# 	cp -r frontend/squeak-node-frontend/build/ ./static/build

RUN python3 setup.py install

EXPOSE 8774
EXPOSE 8994
EXPOSE 18774
EXPOSE 18994
# Web server
EXPOSE 12994

# Copy the entrypoint script.
COPY "docker/sqkserver/start-sqkserver.sh" .
RUN chmod +x start-sqkserver.sh
