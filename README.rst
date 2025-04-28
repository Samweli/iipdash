=======================================================
IIPDash (Integrated Infrastructure Planning Dashboard)
=======================================================

.. image:: https://github.com/tehamalab/iipdash/actions/workflows/pre-commit.yaml/badge.svg
   :target: https://github.com/tehamalab/iipdash/actions/workflows/pre-commit.yaml
   :alt: pre-commit

IIPdash is a digital infrastructure planning and analysis platform aiming to improve the
understanding and decision making process related to digital infrastructure with consideration
of social-economic, climate, environment and other infrastructure factors.

Core technologies used in the platform includes

- Python_
- Django_
- PostgreSQL_


.. contents:: Contents
    :local:


Development Installation
========================

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

3.  Ensure your Python virtual environment is active, and then install the project requirements:

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
