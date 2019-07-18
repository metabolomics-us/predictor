FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04

MAINTAINER Your Name "berlinguyinca@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip git

# always good to update pip
RUN pip3 install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

RUN pip3 install -e .
ENTRYPOINT [ "python3" ]

CMD [ "predictor/app.py" ]