import logging

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name):
    """
    Get a logger with the specified name.
    
    Args:
        name (str): The name of the logger, typically __name__ from the calling module
        
    Returns:
        logging.Logger: A configured logger instance
    """
    return logging.getLogger(name)