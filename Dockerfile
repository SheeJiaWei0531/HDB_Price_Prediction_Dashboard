
FROM python:3.10.6



COPY ./requirements.txt /requirements.txt


RUN pip install --no-cache-dir --upgrade -r /requirements.txt


COPY ./HDB /HDB
RUN pip install --upgrade pip

CMD ["sh", "-c", "uvicorn HDB.api.fast:app --host 0.0.0.0 --port $PORT"]
