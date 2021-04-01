FROM python:3.8

RUN apt-get update
RUN apt-get install -y openvpn unzip
RUN cd /etc/openvpn \
    && wget https://my.surfshark.com/vpn/api/v1/server/configurations \
    && unzip configurations


RUN mkdir __logger

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get -y update \
    && apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99
ENV APP_ENV=development

COPY . /app
WORKDIR /app

# using openvpn
RUN pip install --no-cache-dir -r requirements.txt
RUN printf '${SURFSHARK_USERID}\n${SURFSHARK_PSWD}\n' > auth.txt
RUN find /etc/openvpn -type f -name "*.ovpn" -exec sed -i 's/auth-user-pass/auth-user-pass auth.txt/g' {} +
RUN openvpn "$(find /etc/openvpn -type f -name "*.ovpn" | shuf -n 1)" &

ENTRYPOINT ["python3", "./worker.py", "--from_account", "${from_account}",  "--start_date", "${start_date}"]