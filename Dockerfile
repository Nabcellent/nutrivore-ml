# Backend/Dockerfile
FROM python:3.11.5

RUN mkdir -p app

COPY requirements.txt app/requirements.txt

COPY . app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]