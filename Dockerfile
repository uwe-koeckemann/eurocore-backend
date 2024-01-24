FROM python:3.8-slim-buster

WORKDIR /eurocore
COPY . /eurocore

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["./start.sh"]