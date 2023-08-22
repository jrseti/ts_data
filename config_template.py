# This file contains a template for the config.py file.
# Copy this file to config.py and fill in the values.
import os

# Tradestation API information
API_KEY = "your tradestation api key"
API_SECRET_KEY = "your tradestation secret key"

# Specify where the log files will be located. Make sure this directory
# exists and is writable by the user running the program.
LOG_DIRECTORY = '/location of log directory'
# Specify the log file format
LOG_MESSAGE_FORMAT = "%(created)f %(levelname)-8s %(message)s"

# Redis connection information
REDIS_HOST = "localhost"
REDIS_PORT = 6379