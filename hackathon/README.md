# Sonar

## Start RabbitMQ & Celery Worker
```
rabbitmq-server & celery -A hackathon worker -B
```

## On a Mac (need to install rabbitmq freom homebrew before)
```
brew services restart rabbitmq & celery -A hackathon worker -B
```

## Run the Django Server
```
python3 manage.py runserver
```

## Reset DB
Delete `db.sqlite3` and run `python3 manage.py migrate`