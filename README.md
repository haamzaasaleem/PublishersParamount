# Commands to run celery

    celery -A core worker -l INFO
    
    redis-cli
    
    celery -A core flower  --address=127.0.0.1 --port=5566