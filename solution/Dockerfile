#FROM python:3.12-alpine3.21
FROM python:3.12-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "src.app"]
