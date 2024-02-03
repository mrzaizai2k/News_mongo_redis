# News_mongo_redis
Store news and news summary with MongoDB and Redis

Trello: https://trello.com/b/yiKSwU9w/data-engineering

- `docs`: Cho word and slide
- `src`: source code
- `config`: config file `.yaml`
- `notebook`: Là các file chứa example code

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

2. Nhớ Run docker Redis mỗi khi cần dùng redis database

## Tổng quan hệ thống

1. Hệ thống crawl báo từ 2 nguồn [Zing news](https://znews.vn/) và [CafeF](https://cafef.vn/) suwr dungj Beautiful Soup và Langchain
2. Báo được lưu ở MongoDB với 5 thành phần: title, page_content, publish_date, authors, link 
3. Những Top news sẽ được tổng hợp nhờ model Falcon summary. Qua model summary, redis sẽ lưu thêm 1 trường dữ liệu là summary_text
4. Top news sẽ hiển thị trên UI. Khi người dùng click vào, ta sẽ lấy báo từ redis, hoặc MongoDB