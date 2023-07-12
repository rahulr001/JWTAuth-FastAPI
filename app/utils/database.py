from pymongo.mongo_client import MongoClient
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

client = MongoClient("mongodb+srv://rahul:admin@cluster0.kzbcolz.mongodb.net/")

db = client['oAuth2']
User = db['user']

