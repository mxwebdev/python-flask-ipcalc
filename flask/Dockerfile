FROM python:3-alpine

RUN adduser -D ipcalcflask

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

# Install the dependencies
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install uswgi

RUN chown -R ipcalcflask:ipcalcflask ./
USER ipcalcflask

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]