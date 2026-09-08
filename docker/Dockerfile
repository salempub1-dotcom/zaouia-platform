FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements requirements
ARG REQUIREMENTS_FILE=prod.txt
RUN pip install --upgrade pip \
    && pip install -r requirements/${REQUIREMENTS_FILE}

COPY . .

RUN chmod +x docker/entrypoint.sh \
    && useradd --create-home app \
    && mkdir -p media staticfiles \
    && chown -R app:app /app

USER app

ENTRYPOINT ["sh", "docker/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--access-logfile", "-"]
