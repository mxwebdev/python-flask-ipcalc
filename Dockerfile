FROM python:3-alpine

RUN adduser -D ipcalcflask

WORKDIR /home/ipcalcflask

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY main.py start.sh ./
RUN chmod +x start.sh

ENV FLASK_APP main.py

RUN chown -R ipcalcflask:ipcalcflask ./
USER ipcalcflask

EXPOSE 5000
ENTRYPOINT ["./start.sh"]