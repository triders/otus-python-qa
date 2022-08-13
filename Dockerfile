FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .

CMD ["pytest", "-s", "--base_url", "localhost", "api_data_driven_tests/test_open_brewery_db.py"]
