from motor import motor_asyncio
from pymongo.errors import OperationFailure
  # Настройки подключения, например DATABASE_URL и DATABASE_NAME
# from pymongo import MongoClient

# DATABASE_URL = "mongodb://mongo:27017"  # Укажите URL вашей MongoDB
# DATABASE_URL = "mongodb://mongo:27017/employee_permission"
DATABASE_URL = "mongodb://admin:admin@mongo:27017"
DATABASE_NAME = "employee_permission"  # База данных для сотрудников


# def setup_mongo():
#     mongo_client = MongoClient(
#         host="host",
#         port=27017,
#         username="admin",
#         password="admin"
#     )
#     db = mongo_client["employee_permission"]
#     collection = db["employee"]
#     # collection.create_index([("user_id", ASCENDING)], unique=True)
#     return collection

class Database:
    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
        self.db = self.client[DATABASE_NAME]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]
            
    async def create_index(self, collection_name: str, field_name: str, unique: bool = False):
        collection = self.get_collection(collection_name)
        # Создание индекса на поле
        await collection.create_index([(field_name, 1)], unique=unique)
        print(f"Index created for field {field_name} in collection {collection_name}")



db = Database()