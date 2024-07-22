

pip install celery    

pip install redis    

docker-compose up   # запускаем docker

celery -A tasks.app worker  