FROM python:3.7.1

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
WORKDIR /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD [ "./docker/db-init/wait-for-postgres.sh", "db", "./docker/db-init/startup.sh" ]
