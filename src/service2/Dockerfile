FROM python:3.8

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

EXPOSE 8020

COPY ./service2.py /app/service2.py
COPY config-docker.ini /app/config.ini

WORKDIR /app

CMD ["uvicorn", "service2:app", "--host", "0.0.0.0", "--port", "8020"]