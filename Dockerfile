FROM python:3.10.6

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY HDB /HDB
COPY setup.py /setup.py

# RUN pip install --upgrade pip

CMD uvicorn HDB.api.fast:app --host 0.0.0.0
