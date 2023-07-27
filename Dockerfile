
FROM python:3.10.6


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./HDB /code/HDB
RUN pip install --upgrade pip

CMD ["sh", "-c", "uvicorn HDB.api.fast:app --host 0.0.0.0 --port $PORT"]
