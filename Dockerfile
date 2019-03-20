FROM python:3.6-alpine
RUN apk add --no-cache --update gcc musl-dev librdkafka-dev librdkafka
COPY requirements.txt /
COPY pip.conf /
ENV PIP_CONFIG_FILE="pip.conf"
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app/process_checker
CMD ["python", "main.py"]