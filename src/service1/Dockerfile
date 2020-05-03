FROM python:3.8

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

EXPOSE 8010

COPY ./service1.py /app/service1.py
COPY config-docker.ini /app/config.ini

WORKDIR /app

CMD ["uvicorn", "service1:app", "--host", "0.0.0.0", "--port", "8010"]