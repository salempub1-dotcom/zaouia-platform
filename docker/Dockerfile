FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev gettext && rm -rf /var/lib/apt/lists/*
COPY requirements requirements
RUN pip install --no-cache-dir -r requirements/dev.txt
COPY . .
RUN useradd --create-home app && mkdir -p media staticfiles && chown -R app:app /app
USER app
ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["gunicorn","config.wsgi:application","-b","0.0.0.0:8000","-w","3","--timeout","120"]
