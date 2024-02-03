import redis

import json
import schedule
import time
from datetime import datetime
import threading
from threading import Thread

from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query 

from src.utils import config_parser

class RedisDatabase:
    def __init__(self, host='localhost', port=6379, 
                 database_number = 0, #This will change the db num (we has 16 db)
                 redis_config_path = 'config/redis_db.yaml'):

        self.host = host
        self.port = port
        self.database_number = database_number
        self.redis_config_path = redis_config_path

        self.redis_config = config_parser(data_config_path=self.redis_config_path)
        self.connection = redis.Redis(host=self.host, port=self.port, decode_responses=True)
        self.connection.select(self.database_number)
        print(f'Connected: {self.connection.ping()}')


    def initilize_schema(self):
    
        self.schema = (
            TextField("$.title", as_name="title"), 
            TextField("$.link", as_name="link"), 
            TextField("$.authors", as_name="authors"), 
            TextField("$.publish_date", as_name="publish_date"), 
            TextField("$.page_content", as_name="page_content"), 
            TextField("$.summary_text", as_name="summary_text"), 
            )

        self.rs = self.connection.ft("idx:title")
        self.rs.create_index(
            self.schema,
            definition=IndexDefinition(
                prefix=["title:"], index_type=IndexType.JSON
            )
            )

    def save_news(self, full_news: dict):
        self.connection.json().set(f"title:{full_news['title']}", Path.root_path(), full_news)
        return
    
    def save_news_in_batch(self, full_news_list:list[dict]):
        for full_news in full_news_list:
            self.save_news(full_news=full_news)
        return
    
    
    def get_news_with_title(self, text:str):
        return  self.rs.search(Query(f"@title: {text}"))
    
    def get_news_with_page_content_match(self, text:str):
        return  self.rs.search(Query(f"@page_content: {text}"))
    
    
    def get_news_with_summary_match(self, text:str):
        return  self.rs.search(Query(f"@summary_text: {text}"))
    

    def flush_database(self):
        # Flush the database
        self.connection.flushdb()
        print(f"Database flushed at {datetime.now()}")

    def flush_database_at_schedule(self):
        flush_time = self.redis_config.get('flush_time')
        print('flush_time', flush_time)

        schedule.every().day.at("23:00").do(self.flush_database)

        Thread(target=self.schedule_checker).start() 
    
    def schedule_checker(self):
        # Run the scheduler
        while True:
            schedule.run_pending()
            time.sleep(1)


def main():
    redis_db = RedisDatabase()
    # redis_db.flush_database()


if __name__ == '__main__':
    main()
    
