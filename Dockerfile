FROM python:3.12-slim

WORKDIR /pantip_etl_cronjob

ADD . /pantip_etl_cronjob

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator1 \
    libasound2 \
    libxtst6 \
    libxrandr2 \
    xdg-utils \
    fonts-liberation \
    libu2f-udev \
    libvulkan1 \
    cron\
    libpq-dev\
    gcc\
    && rm -rf /var/lib/apt/lists/*



# Install Chrome version 124
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install matching Chromedriver
RUN CHROME_DRIVER_VERSION=124.0.6367.119 && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

COPY crontab /etc/cron.d/crontab

RUN crontab /etc/cron.d/crontab

RUN pip install -r requirements.txt

CMD ["cron", "-f"]