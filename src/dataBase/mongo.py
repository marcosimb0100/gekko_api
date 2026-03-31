from pymongo import MongoClient
from config import current_config

def cnn_mongo():
    try:
        client  = MongoClient(current_config.MONGO)
        db = client.get_default_database()
        client.admin.command('ping')
        
        return db
    except Exception as ex:
        raise Exception(f"Error al conectar con MONGO DB: {str(ex)}")