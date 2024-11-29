=============
IIP Dashboard
=============

Based on

- Python_
- Django_
- Postgresql_

Development Installation
========================

Database Setup
--------------
PostgreSQL is used as a primary database engine.


On ubuntu or Debian based system to install and start Postgresql you can run something like

.. code:: bash

    sudo apt update
    sudo apt install postgresql postgresql-contrib libpq-dev
    sudo service postgresql start


After installing Postgresql, you will need to initialize the database.

Login as  Postgresql admin user (`postgres`)

.. code:: bash

    sudo su -l postgres


While logged in as `postgres` create the project database

.. code:: bash

    createdb iipdash


Connect to the database shell

.. code:: bash

    psql iipdash


While you are in the database shell create the database user, grant appropriate privileges to the user
and enable the PostGIS plugin.

.. code:: sql

    CREATE USER iipdash WITH PASSWORD 'iipdash';
    GRANT ALL PRIVILEGES ON DATABASE iipdash TO iipdash;
    CREATE EXTENSION postgis;
    exit;


Install system wide Python dependencies
---------------------------------------

Install Python development header files (python-dev) and Python package Installer `pip <https://pip.pypa.io/en/stable>`_

.. code:: bash

    sudo apt install python3-dev python3-pip libz-dev libjpeg-dev libfreetype6-dev


Setup a Python virtual environment
----------------------------------

It is recommended to isolate project dependencies in order to avoid potential
dependency conflicts. One of the simplest ways to achieve that is by using `Python virtual environments <https://realpython.com/python-virtual-environments-a-primer/>`_.

For development installation you may optionally use `Virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ for convenience.

You can create a virtual environment for the project using any of your favorite tools.


Project setup
-------------

Download the source code

.. code:: bash

    git clone git@github.com:tehamalab/iipdash.git


Go to project root

.. code:: bash
    cd iipdash/


make sure your python virtual environment is active then use pip to install project requirements.

.. code:: bash

    pip install -r requirements_dev.txt


Change your project settings according to your preferences typically
by creating a ``.env`` file.

Example; to enable debug mode

.. code:: bash

    # .env file

    DEBUG=True


Check out ``.env.example`` for a sample ``.env`` for development

Project setting can modified using

- System environment variables
- Environment variables written in ``.env`` file at the project root


To check if things are OK run

.. code:: bash

    ./manage.py check


Create database tables

.. code:: bash

    ./manage.py migrate


Create a superuser for admin access

.. code:: bash

    ./manage.py createsuperuser


**NOTE:** When you are executing ``manage.py ...`` commands make sure the virtualenv is active.


Starting the development server
--------------------------------

Django comes with an inbuilt server which can be used during development.
You shouldn't be using this server on production sites.

To start the development server go to your project root directory run

.. code:: bash

    ./manage.py runserver [some-port-number]


Running tests
-------------

To run unit tests make sure you database user has permission to
create a database and extensions.
On your database shell, You can give your user required permissions
using something like:

.. code:: sql

    ALTER ROLE iipdash SUPERUSER;

To run basic unit tests

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

The project can be deployed using a fairly standard Django deployment procedures/setup.
For more information on Django deployment please look for the available resources on the Internet
including https://docs.djangoproject.com/en/5.0/howto/deployment/

You can also use included docker compose configuration for production deployment.
The docker images don’t include deployment of Postgresql,
a queue/message broker (example RabbitMQ) and a proxy server (example Nginx),
therefore those might need to be pre-configured separately.


.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://isort.readthedocs.io/en/latest/
.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/
.. _Postgresql: https://www.postgresql.org/
