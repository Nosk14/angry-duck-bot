FROM python:3.8-slim
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src /usr/local/bot/
WORKDIR /usr/local/bot/
CMD python3 run.py