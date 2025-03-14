import logging

# Create a logger
logger = logging.getLogger("campaign_logger")
logger.setLevel(logging.INFO)

# Create a file handler to log to a file
file_handler = logging.FileHandler("campaign_log.log")
file_handler.setLevel(logging.INFO)

# Create a stream handler to log to the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Define the log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Example usage
logger.info("Logging setup is working!")
