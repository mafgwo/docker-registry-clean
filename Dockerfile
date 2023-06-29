FROM python:3.7.17-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -y install cron

RUN echo "* * * * * root /usr/local/bin/python /app/main.py >> /var/log/cron.log 2>&1" >> /etc/crontab
RUN chmod 0644 /etc/crontab
RUN touch /var/log/cron.log

COPY . .

CMD cron && tail -f /var/log/cron.log
