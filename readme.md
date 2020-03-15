# docker+django+vue+nginx

## Getting Started
you need env/.env.dev or env/.env.prod file.  
example below

```
DEBUG=1
SECRET_KEY=!0$5@7$m5n1-hz+p!vm30#@8cahlm2w4waa=p0o6q8s6=7u-v0
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
DEVELOPER_KEY=change me
```
DEVELOPER_KEY is [api key](https://cloud.google.com/docs/authentication/api-keys)

### dev 

```
docker-compose -f docker-compose.yml up -d --build
``` 
CELERY tasks can be debug, if you use pycharm remote debug and set DEBUG_CELERY=True in app/backend/settings.py  
http://localhost:8000/
### prod 
```
docker-compose -f docker-compose.prod.yml up -d --build
``` 


http://localhost:1337/ 

![title](画面収録.gif)