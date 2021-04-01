FROM python:3.8

RUN mkdir __logger

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get -y update \
    && apt-get install -y google-chrome-stable

# set display port to avoid crash
ENV DISPLAY=:99

COPY . /app
WORKDIR /app

COPY ./deploy/production/.env /app

RUN python3 setup.py install

WORKDIR /app/master-scraper

CMD ["python3", "./master.py"]