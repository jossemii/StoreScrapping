FROM python:3.9
RUN apt-get update
RUN apt-get install -y python3-pip 
RUN apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libxkbcommon0 libgbm1 libpango-1.0-0 libcairo2 libatspi2.0-0 \
    libgtk2.0-0 libxss-dev libgconf-2-4 libasound2 libxshmfence-dev

RUN mkdir /app
COPY . /app/
RUN pip3 install -r /app/requirements.txt
RUN python -m playwright install
RUN adduser user