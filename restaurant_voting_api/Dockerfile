FROM python:3.12.3

WORKDIR /restaurant_voting_api
COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential python3-dev

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "${HOST}:${PORT}"]
