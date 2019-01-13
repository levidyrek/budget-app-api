FROM python:3.7.1

COPY requirements.txt /code/
WORKDIR /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD [ "./docker/api/startup.sh" ]
