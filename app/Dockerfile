FROM pypy:3.10 AS builder

WORKDIR /app

RUN apt-get update

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

CMD ["gunicorn", "-c", "GunicornConfig.py", "main:app"]