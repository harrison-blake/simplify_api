FROM python:3.9-alpine

WORKDIR /usr/src/api/

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /usr/src/api/

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]