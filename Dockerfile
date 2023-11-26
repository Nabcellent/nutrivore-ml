# Backend/Dockerfile
FROM python:3.10.8

RUN mkdir -p app

COPY requirements.txt app/requirements.txt
COPY data app/Data

COPY . app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080","--reload"]