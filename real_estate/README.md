# Real Estate Management

## Feature
1. __Property Module__: reflect all available property

## Technology Stack
1. Python environment: python 3.5.2
1. Framework: Django = 2.2.11
1. UI Technology: HTML, CSS, BS, JS, jQuery

## Installation Set Up
* Click on [install](https://pypi.org/project/virtualenv/) to create virtual environment
* Install python 3.5
```python
            sudo apt-get install python3.5
```
* Install requirement.txt for all project dependencies
* Install postgresql database
```batch
            sudo apt-get install postgresql postgresql-contrib
```

## Create Database

* sudo -u postgres psql
* CREATE DATABASE real_estatedb;
* \l
* \q

## How to use

1. Clone the project
1. Update settings.py file
```python
# Database Configration
            DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'real_estatedb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
3. Use following commands to migrate the table
```python
           python manage.py makemigrations
           python manage.py migrate
```
4. Create super user account using below command
```python
             python manage.py createsuperuser
```
5. SignUp Dealer account using User and DealerRoll from django admin
```python
              Required Information:
              firstname, lastname, username, all password, mobile
```
6. Then start the project directly with following command
```python
              python manage.py runserver 127.0.0.1:8000
              login by Dealer account credentials
```
