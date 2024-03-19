import configparser
import os
  
def get_config(section, key):
    from kognitive_src.utils import logger
    config = configparser.ConfigParser()
   
    config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
    
    if not os.path.exists(config_file_path):
        logger.error("Configuration file not found at path: %s", config_file_path)
        raise FileNotFoundError("Configuration file not found at path: " + config_file_path)
    else:
        logger.info("Found configuration file at path: %s", config_file_path)

    config.read(config_file_path)
    
    if not config.has_section(section):
        logger.error("Section [%s] not found in configuration file.", section)
        raise ValueError(f"Section {section} not found in configuration file.")
    
    if not config.has_option(section, key):
        logger.error("Key %s not found in section [%s].", key, section)
        raise ValueError(f"Key {key} not found in section {section}.")

    value = config.get(section, key)
    logger.info("Configuration for [%s] - %s: %s", section, key, value)
    
    return value
