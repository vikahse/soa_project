FROM python:3.9-slim-buster

RUN pip install --upgrade pip

WORKDIR /backend

RUN export FLASK_APP=app.py
RUN export PGHOST=localhost
RUN export PGPORT=5433

COPY requirements.txt /backend
RUN pip install -r requirements.txt

COPY . /backend

#ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]

