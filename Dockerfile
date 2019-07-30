FROM python:3-alpine

ADD requirements.txt /etc/src/requirements.txt
RUN pip install -U pip setuptools virtualenv  && \
    virtualenv /venv  && \
    source /venv/bin/activate  && \
    which python  && \
    pip install -r /etc/src/requirements.txt
ENV PYTHONHOME=/venv PATH=/venv/bin:$PATH
