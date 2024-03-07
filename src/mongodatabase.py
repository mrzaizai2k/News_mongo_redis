import pymongo

class NewspaperDatabase:
    def __init__(self, connection_string, db_name):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db_name]
        self.articles_collection = self.db["articles"]
    
    def insert_articles(self, newspaper_data):
        result = self.articles_collection.insert_many(newspaper_data)
        return result

    def retrieve_all_articles(self):
        result = self.articles_collection.find()
        return result

    def retrieve_attribute_articles(self,title):
        result = self.articles_collection.find({"title":title})
        return result

if __name__ == "__main__":
    # Example usage
    newspaper_db = NewspaperDatabase()