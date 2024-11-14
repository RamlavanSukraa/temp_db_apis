# config.py

import configparser
from utils.logger import app_logger  
import os


def load_mongo(file_path=None, section='database'):
    if file_path is None:
        # Dynamically determine the path to `config.ini` located in the project root
        file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    if not os.path.exists(file_path):
        app_logger.error(f"Configuration file '{file_path}' not found.")
        raise Exception(f"Configuration file '{file_path}' not found.")

    config = configparser.ConfigParser()
    config.read(file_path)

    if section not in config:
        app_logger.error(f"Section '{section}' not found in the configuration file '{file_path}'.")
        raise Exception(f"Section '{section}' not found in the configuration file '{file_path}'.")

    try:
        config_data = {
            'MONGODB_URI': config.get(section, 'MONGODB_URI'),
            'DATABASE_NAME': config.get(section, 'DATABASE_NAME'),
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
