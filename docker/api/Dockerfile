FROM python:3.7.1

COPY . /code/
WORKDIR /code/

RUN pip install -r requirements.txt

CMD [ "./docker/api/startup.sh" ]
