FROM redis:7.2-alpine

RUN mkdir -p /var/log/redis && \
    chown redis:redis /var/log/redis

COPY redis.conf /usr/local/etc/redis/redis.conf
RUN chown redis:redis /usr/local/etc/redis/redis.conf

EXPOSE 6379

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]