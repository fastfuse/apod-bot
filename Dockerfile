FROM python:3.6

ENV PYTHONUNBUFFERED=0
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT python main.py
