#FROM nvidia/cuda:11.7.0-devel-ubuntu20.04
FROM python:3.11



ARG WORKING_DIR="/home/work"
ARG project_name="poetryDev"
WORKDIR ${WORKING_DIR}

# envi
ENV TZ=Asia/Tokyo

# set timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Step2: poetry config
#env PATH $PATH:$WORKING_DIR/.local/bin
ENV POETRY_HOME=/opt/poetry
ENV PATH $PATH:$WORKING_DIR/.local/bin
RUN apt install curl -y && \
mkdir /opt/poetry/bin -p && \
# apt install python3.9-distutils -y && \
curl -sSL https://install.python-poetry.org | python3.11 -  && \
cd /usr/local/bin && ln -s /opt/poetry/bin/poetry  && \
poetry config virtualenvs.in-project true
#poetry config virtualenvs.create true

#CMD

ENV SHELL=/bin/bash
RUN apt update -y 
RUN apt install vim net-tools sqlite3 build-essential graphviz default-jre fonts-ipafont -y


CMD ["bash"]
