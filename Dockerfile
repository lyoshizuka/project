# app/Dockerfile

FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && apt-get install -y \
    apt-utils \
    # build-essentials \
    curl \
    python3-pip \
    python3-yaml \
    software-properties-common \
    git \

    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/lyoshizuka/project.git .

RUN pip3 install -r requirements.txt

RUN pip3 install --upgrade pip

RUN pip3 install streamlit

COPY / ./

CMD ["streamlit","run","app.py"]
