FROM python:3.12-slim

WORKDIR /pantip_etl_cronjob

ADD . /pantip_etl_cronjob

RUN apt-get update

RUN apt-get install -y cron libpq-dev gcc 

COPY crontab /etc/cron.d/crontab

RUN crontab /etc/cron.d/crontab

RUN pip install -r requirements.txt

CMD ["cron", "-f"]