FROM python:3.12.1
ADD . /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -qq -y python3-opencv libopencv-dev
RUN pip install -r requirements.txt
CMD ["python", "server.py"]
