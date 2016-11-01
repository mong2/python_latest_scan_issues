FROM ubuntu:16.04
MAINTAINER toolbox@cloudpassage.com

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    python-pip && \apt-get install -y git

COPY ./ /source/

WORKDIR /source/

RUN pip install cloudpassage

RUN pip install -r requirements-testing.txt

RUN pip install codeclimate-test-reporter
