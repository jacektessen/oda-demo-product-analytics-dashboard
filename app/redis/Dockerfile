FROM redis:7-alpine

EXPOSE ${REDIS_PORT}

CMD redis-server \
    --port ${REDIS_PORT} \
    --bind 0.0.0.0 \
    --protected-mode no \
    --maxmemory 256mb \
    --maxmemory-policy allkeys-lru \
    --save 900 1 \
    --save 300 10 \
    --save 60 10000 \
    --loglevel notice \
    --tcp-keepalive 300 \
    --databases 16