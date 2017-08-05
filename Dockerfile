FROM python:3.5.3-alpine

RUN pip3 install pytest-flask==0.10.0 \
    Flask==0.12.2 \
    flask-cors==3.0.3 \
    requests==2.9.1 \
    requests-mock==1.3.0

ADD ./flask /code/src

WORKDIR /code/src

CMD python app.py