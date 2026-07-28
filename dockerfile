FROM python:3.11-alpine
RUN apk add --no-cache iputils

WORKDIR /app
COPY main.py .
COPY targets.txt .

ENTRYPOINT ["python", "main.py"]
