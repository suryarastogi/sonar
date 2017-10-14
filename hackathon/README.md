# Sonar

## Start RabbitMQ & Celery Worker
```
rabbitmq-server & celery -A hackathon worker -B
```

## On a mac
```
brew services restart rabbitmq & celery -A hackathon worker -B
```

## Run the Django Server
```
python3 manage.py runserver
```