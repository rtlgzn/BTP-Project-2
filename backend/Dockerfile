FROM python:3.8-slim-buster
WORKDIR /app
ADD . /app
RUN apt-get update && apt-get install -y sqlite3 && \
    pip install --no-cache-dir python-dotenv bcrypt jwt
EXPOSE 8000
CMD ["python", "server.py"]
