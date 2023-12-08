FROM python:latest

RUN pip install dash redis

WORKDIR /app
COPY . /app

EXPOSE 31215

CMD ["python", "dashboard.py", "--host=0.0.0.0"]