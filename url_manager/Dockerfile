FROM python:3.12-slim

WORKDIR /url_manager

COPY requirements.txt requirements.txt
RUN pip3 install -r ./requirements.txt

COPY . /url_manager 

CMD [ "python3", "main.py"]

