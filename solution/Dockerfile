FROM python:3.12-alpine3.21

#WORKDIR /solution

COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY . .
COPY . .

#ENV PYTHONPATH=/usr/src/app/src

#CMD ["python", "src/app.py"]
CMD ["python", "-m", "src.app"]
