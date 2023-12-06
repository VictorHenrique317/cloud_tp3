FROM python:latest

RUN pip install dash redis

WORKDIR /app
COPY . /app

EXPOSE 8050

CMD ["python", "dashboard.py", "--host=0.0.0.0"]