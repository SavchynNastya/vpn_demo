FROM python:3.11-buster

RUN apt-get update \
  && apt-get install -y libpq-dev git curl \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /app_vpn
WORKDIR /app_vpn

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD . /app_vpn

RUN pip install -r conf/requirements.txt

EXPOSE 8000

RUN ["chmod", "+x", "./entrypoint-local.sh"]
ENTRYPOINT ["./entrypoint-local.sh"]