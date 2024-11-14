import configparser
from utils.logger import app_logger  # Import the logger instance

def load_config(file_path='config.ini', section='database'):

    config = configparser.ConfigParser()
    config.read(file_path)

    if section not in config:
        app_logger.error(f"Section '{section}' not found in the configuration file '{file_path}'.")
        raise Exception(f"Section '{section}' not found in the configuration file '{file_path}'.")

    try:
        config_data = {
            'MONGO_URI': config.get(section, 'MONGODB_URI'),
            'DB_NAME': config.get(section, 'DATABASE_NAME'),
            'COLLECTION_NAME': config.get(section, 'COLLECTION_NAME'),
            'MONGODB_USERNAME': config.get(section, 'MONGODB_USERNAME', fallback=None),
            'MONGODB_PASSWORD': config.get(section, 'MONGODB_PASSWORD', fallback=None)
        }
        
        app_logger.info("Configuration loaded successfully.")
        return config_data

    except KeyError as e:
        app_logger.error(f"Configuration error: Missing key {e}")
        raise Exception(f"Configuration error: Missing key {e}")
    except Exception as e:
        app_logger.error(f"Unexpected error while loading configuration: {e}")
        raise Exception(f"Unexpected error while loading configuration: {e}")
