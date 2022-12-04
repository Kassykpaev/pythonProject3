FROM python:3.7

RUN mkdir -p /usr/src/app/db

WORKDIR /usr/src/app/
ENV TELEGRAM_API_TOKEN="5860387720:AAEpxIgJscA3cb3yZJkz876I7Y4c9hvmerE"
ENV DB_NAME="sqlite.db"

COPY *.py /usr/src/app/
COPY kassymtelegrambot.json /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]