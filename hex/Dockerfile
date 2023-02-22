FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /drf-app

COPY requirements.txt /drf-app/
RUN pip install -r requirements.txt
COPY . /drf-app/