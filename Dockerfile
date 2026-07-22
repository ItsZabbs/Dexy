FROM debian:12-slim
FROM python:3.14-slim
RUN apt-get update && apt-get install -y git
RUN apt-get install -y postgresql postgresql-contrib
WORKDIR /Pokedex-Bot

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python3","launcher.py"]
