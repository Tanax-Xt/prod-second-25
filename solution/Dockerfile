FROM python:3.12-alpine3.21

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/usr/src/app/src
CMD ["python", "./src/app.py"]
