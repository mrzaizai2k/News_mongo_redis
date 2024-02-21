import pymongo

class NewspaperDatabase:
    def __init__(self, connection_string, db_name):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db_name]
        self.articles_collection = self.db["articles"]
    
    def insert_articles(self, newspaper_data):
        result = self.articles_collection.insert_one(newspaper_data)
        return result

if __name__ == "__main__":
    # Example usage
    newspaper_db = NewspaperDatabase()