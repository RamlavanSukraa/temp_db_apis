from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from config import load_config, app_logger

# Initialize a variable to store the client and collection
_mongo_client = None
_mongo_collection = None

def connect_to_mongo(file_path='config.ini', section='database'):
    global _mongo_client, _mongo_collection

    try:
        # Only create a new connection if it hasn't been initialized yet
        if _mongo_client is None or _mongo_collection is None:
            # Load configuration data
            config_data = load_config(file_path, section)
            mongodb_uri = config_data['MONGO_URI']

            # Construct the URI if credentials are provided
            if config_data['MONGODB_USERNAME'] and config_data['MONGODB_PASSWORD']:
                mongodb_uri = f"mongodb://{config_data['MONGODB_USERNAME']}:{config_data['MONGODB_PASSWORD']}@{mongodb_uri.split('://')[1]}"

            # Connect to MongoDB
            _mongo_client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
            db = _mongo_client[config_data['DB_NAME']]
            _mongo_collection = db[config_data['COLLECTION_NAME']]

            app_logger.info(f"Database {config_data['DB_NAME']} and collection {config_data['COLLECTION_NAME']} connected successfully!")

        # Return the existing connection if already initialized
        return _mongo_client, _mongo_collection

    except ServerSelectionTimeoutError as e:
        app_logger.error(f"MongoDB server selection timeout: {e}")
        raise
    except PyMongoError as e:
        app_logger.error(f"MongoDB connection error: {e}")
        raise
    except Exception as e:
        app_logger.error(f"An unexpected error occurred while connecting to MongoDB: {e}")
        raise
