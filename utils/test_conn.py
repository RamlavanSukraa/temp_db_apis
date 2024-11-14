import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.mongo_conn import connect_to_mongo
from utils.logger import app_logger

# Use the configured logger from utils
logger = app_logger

def test_mongo_connection():
    
    try:
        # Attempt to connect to MongoDB
        client, collection = connect_to_mongo()
        
        # Log and print basic information to confirm the connection
        logger.info("MongoDB connection test successful.")
        
        print(f"Connected to database: {collection.database.name}")
        print(f"Using collection: {collection.name}")

    except Exception as e:
        logger.error(f"MongoDB connection test failed: {e}")
        print(f"MongoDB connection test failed: {e}")

# Run the function only if this script is executed directly
if __name__ == "__main__":
    test_mongo_connection()
