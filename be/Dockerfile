# be/Dockerfile
FROM python:3.9


RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x init.sh
CMD ["sh", "-c", "./init.sh"]
# CMD ["sh", "-c", "python seed_database.py && python app.py"]
# CMD ["python3 app.py"]
