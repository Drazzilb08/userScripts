import os
import time
import logging
import logging.handlers
import pathlib

import logging
import logging.handlers
import os
import pathlib
import time

# Get the parent directory of the script file
base_dir = pathlib.Path(__file__).parents[1]

def setup_logger(log_level, script_name):
    """
    Setup the logger.
    
    Parameters:
        log_level (str): The log level to use
        script_name (str): The name of the script
    
    Returns:
        A logger object for logging messages.
    """
    # Define the directory for log files based on script name
    log_dir = f'{base_dir}/logs/{script_name}'
    
    # Create the log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Get today's date for log file naming
    today = time.strftime("%Y-%m-%d")
    
    # Define the log file path with the current date
    log_file = f"{log_dir}/{script_name}_{today}.log"
    
    # Create a logger object with the script name
    logger = logging.getLogger(script_name)
    logger.propagate = False 
    
    # Set the log level based on the provided parameter
    log_level = log_level.upper()
    if log_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif log_level == 'INFO':
        logger.setLevel(logging.INFO)
    elif log_level == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
    else:
        logger.critical(f"Invalid log level '{log_level}', defaulting to 'INFO'")
        logger.setLevel(logging.INFO)
    
    # Define the log message format
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(message)s', datefmt='%I:%M %p')
    
    # Create a TimedRotatingFileHandler for log files
    handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=3)
    handler.setFormatter(formatter)
    
    # Add the file handler to the logger
    logger.addHandler(handler)
    
    # Configure console logging with the specified log level
    console_handler = logging.StreamHandler()
    if log_level == 'DEBUG':
        console_handler.setLevel(logging.DEBUG)
    elif log_level == 'INFO':
        console_handler.setLevel(logging.INFO)
    elif log_level == 'CRITICAL':
        console_handler.setLevel(logging.CRITICAL)
    
    # Add the console handler to the logger
    logger.addHandler(console_handler)
    
    # Remove older log files, keeping only the latest 3 log files
    log_files = [f for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f)) and f.startswith(f"{script_name}_")]
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(log_dir, x)), reverse=True)
    for file in log_files[3:]:
        os.remove(os.path.join(log_dir, file))
    
    # Add the file handler again (may be redundant, as it's added earlier)
    logger.addHandler(handler)
    
    return logger

