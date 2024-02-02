import sys
sys.path.append("")
import redis

import schedule
import time
from datetime import datetime
import threading
from threading import Thread


from utils import config_parser

class RedisDatabase:
    def __init__(self, host='localhost', port=6379, redis_config_path = 'config/redis_db.yaml'):

        self.host = host
        self.port = port
        self.redis_config_path = redis_config_path
        self.redis_config = config_parser(path=self.redis_config_path)
        self.connection = redis.Redis(host=self.host, port=self.port, decode_responses=True)
        print(f'Connected: {self.connection.ping()}')

    def update_empno(self, emp_no: int, db_num=0):
        # Get the current datetime
        self.connection.select(db_num)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Update emp_no and current time in Redis
        self.connection.hmset(emp_no, {'emp_no': emp_no, 'timestamp': current_time})
        # print(f"Employee {emp_no} updated in Redis at {current_time}")

    def is_empno_exists(self, emp_no: int, db_num=0):
        self.connection.select(db_num)
        # Get the hash values associated with the emp_no
        emp_data = self.connection.hgetall(emp_no)

        if not emp_data:
            return False
        else:
            return True

    def flush_database(self):
        # Flush the database
        self.connection.select(0)
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
    redis_db.is_empno_exists(emp_no=11835)
    redis_db.flush_database()
    redis_db.flush_database_at_schedule()


if __name__ == '__main__':
    main()
    
