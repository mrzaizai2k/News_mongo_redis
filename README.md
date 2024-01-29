# News_mongo_redis
Store news and news summary with MongoDB and Redis

Trello: https://trello.com/b/yiKSwU9w/data-engineering

- `docs`: Cho word and slide
- `src`: source code
- `config`: config file `.yaml`

## Set up Redis

Reference:

- https://redis.io/docs/connect/clients/python/
- https://redis.io/docs/install/install-stack/docker/

1. Cài docker

        docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
        docker exec -it <3 chữ cái đầu của docker container_id> sh
        redis-cli
        ping
        --> Ra Pong là ok