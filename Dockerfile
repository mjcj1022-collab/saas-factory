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

# Collect static — ignore errors if DB not connected at build time
RUN python manage.py collectstatic --noinput \
    --settings=config.settings_prod 2>/dev/null || true

EXPOSE 8000

CMD ["sh", "-c", \
    "python manage.py migrate --noinput && \
     python manage.py create_admin && \
     gunicorn config.wsgi:application \
       --bind 0.0.0.0:${PORT:-8000} \
       --workers 2 \
       --timeout 120 \
       --access-logfile -"]
