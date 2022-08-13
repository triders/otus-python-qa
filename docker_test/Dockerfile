FROM python:3.8-slim

WORKDIR /app

RUN pip install pytest

COPY . .

EXPOSE 8888

CMD ["pytest", "-s", "test_my_app.py"]
