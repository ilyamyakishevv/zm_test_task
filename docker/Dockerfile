FROM python:3.11.8-alpine3.19


RUN apk update && apk add --no-cache \
    gcc g++ musl-dev postgresql-dev libffi-dev build-base


WORKDIR /app


COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt


COPY . /app


WORKDIR /app/

EXPOSE 8000

CMD ["python", "app/main.py"]