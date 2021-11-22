
# Rifa Mais


## At first run:

As part of deploying your application you’ll need to run ./manage.py collectstatic to put all your static files into STATIC_ROOT. (If you’re running on Heroku then this is done automatically for you.)
source: http://whitenoise.evans.io/en/stable/django.html

- Run migrations
 `python manage.py migrate`


- Create superuser
 `python manage.py createsuperuser`


- Create client_id and client_secret for frontend app:
https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html#authorization-code


## Environment variables
The sample `.env.example` file is located at the /rifa_mais/ level . The `.env` file must be located at the same level
> please, request .env keys to a collaborator