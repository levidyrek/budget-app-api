FROM python:3.7.1

WORKDIR /code/

RUN pip install -r requirements.txt

CMD [ "./docker/db-init/startup.sh" ]
