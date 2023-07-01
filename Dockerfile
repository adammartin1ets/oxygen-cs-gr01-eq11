FROM python:3.9-slim

# Install PostgreSQL client and other dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
