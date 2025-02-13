FROM python:3.12.9-slim-bullseye as python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    gettext \
    libssl-dev \
    binutils \
    proj-bin \
    proj-data \
    gdal-bin \
    libgeos-dev \
    libproj-dev \
    libgdal-dev \
    openssl \
    build-essential \
    libjpeg-dev \
    libfreetype6-dev \
    libtiff-dev \
    zlib1g-dev \
    libxslt1-dev \
    git


ARG APP_HOME=/iipdash
WORKDIR ${APP_HOME}

RUN addgroup --system iipdash \
    && adduser --system --ingroup iipdash iipdash

# Install Python requirements
COPY requirements* .
RUN pip install --upgrade pip
RUN pip install -r ./requirements_production.txt

COPY --chown=iipdash:iipdash ./docker/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/production/django/celery/worker/start /start-celery-worker
RUN sed -i 's/\r$//g' /start-celery-worker
RUN chmod +x /start-celery-worker


COPY ./docker/production/django/celery/beat/start /start-celery-beat
RUN sed -i 's/\r$//g' /start-celery-beat
RUN chmod +x /start-celery-beat


COPY ./docker/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

COPY . $APP_HOME

RUN chown -R iipdash:iipdash ${APP_HOME}

ENTRYPOINT ["/entrypoint"]
