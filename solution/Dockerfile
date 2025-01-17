FROM python:3.12-alpine3.21

WORKDIR solution

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "/src/app.py" ]
