===========================
Installation Guide
===========================

This document explains how to install, run and setup the **IIPDash (Integrated Infrastructure Planning Dashboard)** for development.
Two installation methods are provided:

- **Docker installation** - straightforward and consistent setup.
- **Manual installation** - intended for developers and advanced users.

For an overview of platform features and purpose, see :doc:`../readme`.

Core technologies used in the platform includes

- Python
- Django
- PostgreSQL_
- Docker


.. contents:: **Contents**
    :local:



Docker Installation (Recommended)
=================================

Using Docker is the recommended way to install IIPDash. It minimizes system-level dependencies
and provides a consistent development environment across operating systems.

Prerequisites
-------------

Ensure the following tools are installed:

- Docker
- Docker Compose

Installation guides:

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

Verify installation:

.. code:: bash

   docker --version
   docker compose --version

If docker and docker compose are all installed and setup properly, the above commands should display the following respectively

.. code:: bash

    docker --version
    Docker version `version`, build `build_id`

    docker compose --version
    Docker Compose version `version`


Development
-----------

For local development using Docker, use the folllowing configurations and setup:

Make sure to run the below docker commands at the project root. 

The following command builds all necessary Docker images, creates containers for each service and finally starts all services.
Make sure to have internet connection on when running the below command for the first time. This is because the command will
fetch Docker base images from Docker Hub and Python packages from PyPI and install some system packages.

All commands below should be executed from the project root directory.

1. Clone the repository:

   .. code:: bash

      git clone https://github.com/tehamalab/iipdash.git
      cd iipdash

2. Build and start the development environment:

   .. code:: bash

      docker compose -f docker-compose-development.yaml up --build

   The first run may take several minutes while images and dependencies are downloaded.

After successfully running the above command the following services should be up and running.

.. list-table:: Services and Port Mapping
   :header-rows: 1
   :widths: 25 35 15 15

   * - Service
     - Purpose
     - Host Port
     - Container Port
   * - iipdash-dev-django
     - Main application
     - 8000
     - 8000
   * - iipdash-dev-docs
     - Sphinx documentation
     - 9000
     - 9000
   * - iipdash-dev-pg
     - Development database
     - 6432
     - 5432
   * - iipdash-test-pg
     - Test database
     - 7432
     - 5432
   * - iipdash-dev-rabbitmq
     - Message broker
     - 6672
     - 5672
   * - iipdash-dev-redis
     - Cache and background tasks
     - 7379
     - 6379


3. Once started successfully:

   - Open http://0.0.0.0:8000 to access the application
   - Admin interface: http://0.0.0.0:8000/admin

Running Commands in Docker Containers
-------------------------------------

After successfully starting the IIPDash services and they are up and running. Run the below commands to apply migrations, 
prepare database with superusers and run tests before using the application.

Apply database migrations:

.. code:: bash

   docker compose -f docker-compose-development.yaml exec iipdash-dev-django ./manage.py migrate

Create a superuser:

.. code:: bash

   docker compose -f docker-compose-development.yaml exec iipdash-dev-django ./manage.py createsuperuser

Run tests (optional):

.. code:: bash

   docker compose -f docker-compose-development.yaml exec iipdash-dev-django ./manage.py test apps

Start Celery worker (optional but required for some features):

.. code:: bash

   docker compose -f docker-compose-development.yaml exec iipdash-dev-django celery -A iipdash worker -l info


Remember to pass the target docker compose configuration file eg. `docker-compose-development.yaml`. This will ensure docker compose
uses the correct docker configurations to create and access the required services.


Stopping Docker Services
------------------------

Stop all running services:

.. code:: bash

   docker compose -f docker-compose-development.yaml down

Stop services and remove volumes (including database data):

.. code:: bash

   docker compose -f docker-compose-development.yaml down -v


Viewing Logs
------------

View logs from all services:

.. code:: bash

   docker compose logs -f

View logs for a specific service:

.. code:: bash

   docker compose logs -f iipdash-dev-django


Building Docker Image Manually
______________________________


If you want to build the Docker image without starting containers:

.. code:: bash

    docker build -f docker/Dockerfile -t iipdash:latest .

Then run it with custom settings:

.. code:: bash

    docker run -p 8000:8000 \
        -e DEBUG=False \
        -e SECRET_KEY=your-secret-key \
        iipdash:latest

Common Issues
-------------

- Port `number` already in use:
  Stop the application and edit docker configuration files to use a different port.

- Docker command not found:
  Ensure Docker is installed and restarted.

- Page does not load:
  Check that containers are running using `docker compose ps` command.




Manual Installation (Advanced)
==============================

Manual installation is recommended only for developers who require full control over their environment
or cannot use Docker.

Installing IIPdash in your local machine for development involves

* Database setup.
* Installing system-wide dependencies.
* Creating a Python virtual environment.
* Project code set up.
* Starting the development server.


Database Setup
--------------

PostgreSQL
__________
PostgreSQL is used as the primary database engine.

On Ubuntu or Debian-based systems, you can install and start PostgreSQL by running:

.. code:: bash

    sudo apt update
    sudo apt install postgresql postgresql-contrib libpq-dev
    sudo service postgresql start


After installing PostgreSQL, you'll need to initialize the database.

1.  Log in as the PostgreSQL admin user (`postgres`):

    .. code:: bash

        sudo su -l postgres

2.  Create the project database:

    .. code:: bash

        createdb iipdash

3.  Connect to the database shell:

    .. code:: bash

        psql iipdash

4.  While in the database shell, create a database user, grant the necessary privileges,
    and enable the PostGIS and PostGIS Raster extensions:

    .. code:: sql

        CREATE USER iipdash WITH PASSWORD 'iipdash';
        GRANT ALL PRIVILEGES ON DATABASE iipdash TO iipdash;
        CREATE EXTENSION postgis;
        CREATE EXTENSION postgis_raster;
        exit;


Redis (Optional)
________________
By default the platform uses Redis_ as a secondary storage for cache and background tasks processing.
Both cache and background tasks processing storage backend can be switched to other options instead
of Redis_. For more information please consult documentations for Django caching configuration and Celery
message brokers configuration.

To install and start Redis On Ubuntu or Debian-based systems you can run:

.. code:: bash

    sudo apt install redis-server
    sudo systemctl enable redis-server
    sudo systemctl start redis-server

For more information about redis installation options please consult the online documentation.


Install System-Wide dependencies
--------------------------------

Install Python development header files (python-dev) and
Python package Installer `(pip) <https://pip.pypa.io/en/stable>`_

.. code:: bash

    sudo apt install build-essential python3-dev python3-pip

Install other system wide dependencies which including various shared libraries and development headers

.. code:: bash

    sudo apt install binutils proj-bin proj-data libproj-dev gdal-bin libgdal-dev libgeos-dev libjpeg-dev libfreetype6-dev libtiff-dev zlib1g-dev libxslt1-dev gettext openssl libssl-dev


Setup a Python virtual environment
----------------------------------

It is highly recommended to isolate project dependencies in order to avoid potential conflicts.
A common way to achieve this is by using
`Python virtual environments <https://realpython.com/python-virtual-environments-a-primer/>`_.

For development installations, you may optionally use
`Virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ for convenience.

You can create a virtual environment for the project using any of your favorite tools.

Project Setup
-------------

To set up the project:

1.  Download the source code: For example, by cloning directly from GitHub.

    .. code:: bash

        git clone https://github.com/tehamalab/iipdash.git

2.  Navigate to the project root directory:

    .. code:: bash

        cd iipdash/

3.  Ensure your Python virtual environment is active and then install the project requirements:

    .. code:: bash

        pip install -r requirements_dev.txt

4.  Configure your project settings, typically by creating a ``.env`` file.

    Example ``.env`` file (to enable debug mode):

    .. code:: bash

        # .env file
        DEBUG=True

    For a more comprehensive example of a development configuration, refer to the ``.env.example`` file.

    Project settings can be modified using:

    * System environment variables
    * Environment variables in the ``.env`` file at the project root

5.  To check if the setup is correct, run:

    .. code:: bash

        ./manage.py check

6.  Create the database tables:

    .. code:: bash

        ./manage.py migrate

7.  Create a superuser account for admin access:

    .. code:: bash

        ./manage.py createsuperuser


**Note:** Always ensure your virtual environment is active when executing ``manage.py ...`` commands.


Starting the Development Server
--------------------------------
Django includes a built-in development server.  This server should **not** be used for production deployments.

To start the development server, navigate to the project root directory and run:

.. code:: bash

    ./manage.py runserver [optional-port-number]

    For example:

    .. code:: bash

        ./manage.py runserver 8080


Starting Celery
-----------------

The project used Celery for processing some of the tasks asynchronously,
therefore for some features to function properly, you may need to start the celery worker.

To start celery worker you can run

.. code:: bash

    celery -A iipdash worker -l info

By default celery is configured to use Redis_ as a main queue/message broker.
For more information about Celery_ including configuration to use other brokers
please refer to various available online resources including the official celery documentation


Running Tests
-------------

To run unit tests make sure you database user has permission to
create a database and extensions.
In your PostgreSQL shell, you can grant these privileges with a command similar to:

.. code:: sql

    ALTER ROLE iipdash SUPERUSER;

To run project's unit tests

.. code:: bash

    ./manage.py test apps

To check Python coding style, use flake8_

.. code:: bash

    flake8

To automatically sort imports, use isort_

.. code:: bash

    isort .


Deployment
==========

The project can be deployed using standard Django deployment procedures.
For more comprehensive information on Django deployment, please refer to the official `Django Deployment Documentation <https://docs.djangoproject.com/en/5.0/howto/deployment/>`_.

The project also includes a Docker Compose configuration for production deployment.

However, this configuration does **not** include the deployment of:

* PostgreSQL database
* A queue/message broker for celery (e.g., RabbitMQ or Redis)
* A cache storage (e.g., Redis)
* A proxy server (e.g., Nginx)

These components could be configured separately for your production environment.

You build and start a production instance using docker compose, you configure various relevant
environment variables using ``.env`` file at the project root then run

.. code:: bash

    docker compose up --build


.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://isort.readthedocs.io/en/latest/
.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/
.. _PostgreSQL: https://www.postgresql.org/
.. _Celery: https://docs.celeryq.dev/en/stable/
.. _Redis: https://redis.io/



Notes
-----

- The Django development server is **not suitable for production**
- Production deployments require additional services such as a database, cache and reverse proxy
- See Django deployment documentation for production guidance
