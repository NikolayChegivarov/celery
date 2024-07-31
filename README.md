

pip install celery    

pip install redis    

docker-compose up   # запускаем redis из docker

celery -A tasks worker --loglevel=info   # Процесс, который слушает очередь задач и выполняет их/