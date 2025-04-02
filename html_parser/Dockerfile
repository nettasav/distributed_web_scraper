FROM python:3.12-slim

WORKDIR /html_parser

COPY requirements.txt requirements.txt
RUN pip3 install -r ./requirements.txt

COPY . /html_parser 

CMD [ "python3", "main.py"]

