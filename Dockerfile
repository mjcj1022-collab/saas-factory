FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Collect static — won't fail if DB not connected
RUN python manage.py collectstatic --noinput \
    --settings=config.settings_prod 2>/dev/null || true

EXPOSE 8000

# Use --preload so gunicorn starts listening BEFORE workers fully init
# This allows healthcheck to pass while migrations run in foreground first
ENTRYPOINT ["./entrypoint.sh"]
