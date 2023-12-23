FROM python:3.10-alpine

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    bash \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-base


# Copy the entire project directory into the container
COPY . .

COPY wait-for-mongo.sh /wait-for-mongo.sh
RUN chmod +x /wait-for-mongo.sh

EXPOSE 8000

CMD ["sh", "-c", "/wait-for-mongo.sh mongodb:27017 -- python manage.py runserver 0.0.0.0:8000"]

