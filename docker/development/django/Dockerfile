# Reference: https://docs.docker.com/engine/reference/builder/#syntax
# syntax=docker/dockerfile:1

# Use Debian Bookworm with Python 3.12.8 as the base development image
FROM python:3.12.8-slim-bookworm as python

# Image metadata
LABEL maintainer="Tehamalab <engineering@tehamalab.com>" \
      vendor="Tehamalab" \
      description="Development environment for iipdash project"

# Environment variables
# - LANG, LC_ALL, LANGUAGE: Set locale to ensure consistent UTF-8 settings
# - USER_UID, USER_GID: Default UID and GID for creating a non-root user
# - USER_NAME, USER_GROUP: Default username and group name
# - DEBIAN_FRONTEND: Set to noninteractive to disable interactive prompts
# - PYTHONUNBUFFERED, PYTHONDONTWRITEBYTECODE: Improve Python behavior for containers
# - PYTHONFAULTHANDLER, PYTHONHASHSEED: Useful for debugging and deterministic Python behavior
# - RANDOM_SEED: Ensures reproducibility for processes relying on random data
# - TZ: Default timezone to UTC
ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    USER_UID=1000 \
    USER_GID=1000 \
    USER_NAME=iipdash \
    USER_GROUP=iipdash \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=42 \
    RANDOM_SEED=42 \
    TZ=UTC \
    USER_HOME=/home/iipdash \
    APP_HOME=/home/iipdash/iipdash \
    PIP_CACHE_DIR=/home/iipdash/.cache/pip

# Install required system dependencies
# - apt-transport-https: Enables fetching packages over HTTPS
# - binutils, build-essential: Tools for building software (C/C++ libraries)
# - gdal-bin, libgdal-dev, libproj-dev: GIS libraries for working with spatial data
# - libgeos-dev: Geometry engine library required for GIS operations
# - libenchant-2-dev: Wrapper library for various spell checker engines
# - libfreetype6-dev, libjpeg-dev, libtiff-dev, zlib1g-dev: Image processing dependencies
# - libpq-dev: PostgreSQL client libraries for psycopg2
# - libxslt1-dev: XML and XSLT processing library
# - gettext: Required for localization in Django
# - locales: Enables locale generation
# - tzdata: Timezone data configuration
# - git: Version control system
# - openssl: Cryptographic tools
# - sudo: Grants administrative privileges
# - wait-for-it: Script to wait for dependent services (e.g., database)
# hadolint ignore=DL3008
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    set -eux && \
    apt-get update && \
    apt-get install -y --fix-missing --no-install-recommends \
        apt-transport-https \
        binutils \
        build-essential \
        gdal-bin \
        gettext \
        git \
        libenchant-2-dev \
        libfreetype6-dev \
        libgdal-dev \
        libgeos-dev \
        libjpeg-dev \
        libpq-dev \
        libproj-dev \
        libssl-dev \
        libtiff-dev \
        libxslt1-dev \
        locales \
        openssl \
        proj-bin \
        proj-data \
        python3-dev \
        sudo \
        tzdata \
        wait-for-it \
        zlib1g-dev \
    && \
    # Generate and configure locale
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 && \
    # Configure timezone
    ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    # Upgrade and Clean up APT cache to reduce image size
    apt-get -y upgrade --no-install-recommends && \
    apt-get -y autoremove && \
    apt-get -y autoclean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
# - Create a group with the specified `USER_GUID` and `USER_GROUP`
# - Create a user with specified `USER_UID` and `USER_NAME`
# - Ensure the `USER_HOME` directory exists
# - Create `PIP_CACHE_DIR` directory
# - Create `APP_HOME` directory
# - Set `USER_HOME`, `APP_HOME`, ownership to non-root user
RUN groupadd -g ${USER_GID} ${USER_GROUP} && \
    useradd -l -g ${USER_GID} -m -N -u ${USER_UID} -s /bin/bash ${USER_NAME} && \
    mkdir -p ${PIP_CACHE_DIR} && \
    mkdir -p ${APP_HOME} && \
    chown -R ${USER_NAME}:${USER_GROUP} ${USER_HOME}

# Set working directory to the app's home directory
WORKDIR ${APP_HOME}

# Copy, configure, and set permissions for entrypoint, start, and docs scripts
COPY --chown=${USER_NAME}:${USER_GROUP} ./docker/development/django/entrypoint \
     ./docker/development/django/start \
     ./docker/development/docs/start-docs /
RUN sed -i 's/\r$//g' /entrypoint /start /start-docs && \
    chmod +x /entrypoint /start /start-docs

# Copy requirements files with proper ownership
# Upgrade pip and install dependencies
COPY --chown=${USER_NAME}:${USER_GROUP} requirements.txt \
     requirements_dev.txt requirements_docs.txt ./
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip install --cache-dir=${PIP_CACHE_DIR} --upgrade pip && \
    pip install --cache-dir=${PIP_CACHE_DIR} -r requirements_dev.txt && \
    pip install --cache-dir=${PIP_CACHE_DIR} -r requirements_docs.txt

# Switch to the non-root user for security
USER ${USER_NAME}

# Set the default entrypoint
ENTRYPOINT ["/entrypoint"]
